import os
from dotenv import load_dotenv
import requests
import json
import re

load_dotenv()

async def classify_user_query(user_query: str) -> str:
    print("Entering classify_user_query method")
    
    prompt = """You are a classification assistant for BKPM Indonesia's OSS system.

CRITICAL RULES:
1. You MUST respond with ONLY a JSON object - no markdown, no explanations
2. You MUST use categories EXACTLY from the list below - DO NOT create new categories and sub categories
3. Format: {"category": "exact_name", "sub_category": "exact_name"}
4. DETAIL is ONLY context to help you classify - DO NOT use DETAIL text as sub_category

KEY TERMS:
- OSS = Online Single Submission (Indonesian government licensing platform)
- NIB = Nomor Induk Berusaha (official bussiness identity)
- KBLI = Klasifikasi Baku Lapangan Usaha Indonesia
- PB-UMKU = Perizinan Berusaha Untuk Menunjang Kegiatan Usaha
- AHU = Administrasi Hukum Umum (Kementerian Hukum dan HAM)
- RDTR = Rencana Detail Tata Ruang

CLASSIFICATION GUIDE:
category: Pendaftaran
   sub_category: Gagal Melakukan Pendaftaran
   DETAIL: data tidak ditemukan AHU/Dukcapil, gagal input NPWP 16 digit, NIK tidak terdaftar/melebihi kuota, NIK/NPWP sudah terdaftar di akun lain, lupa akun, kendala pendaftaran KDMP/KMP
   sub_category: Panduan Pendaftaran
   DETAIL: cara mendapatkan akun OSS, cara pendaftaran KDMP/KMP
   sub_category: Pendaftaran Baru
   DETAIL: cara pengajuan BUM Desa, cara pengajuan Kantor Perwakilan

category: Log in
   sub_category: Kendala Log in
   DETAIL: gagal login dengan nomor HP/email/username, login gagal karena informasi belum lengkap, kendala resend email login

category: Reset Password
   sub_category: Reset Password
   DETAIL: cara reset password, kendala sistem reset password

category: Ubah Email atau Nomor Ponsel
   sub_category: Perubahan Email tanpa Log in
   DETAIL: ubah email/nomor tanpa login (badan usaha/perorangan), cara dan progres perubahan, kendala sistem/pengguna, perubahan penanggung jawab, email tidak berubah meski disetujui, status dalam/melewati SLA
   sub_category: Perubahan No Ponsel tanpa Log in
   DETAIL: cara ubah nomor ponsel perorangan tanpa login, kendala pengguna/sistem

category: Profil Pelaku Usaha
   sub_category: Perubahan Melalui Profil
   DETAIL: cara ubah email/nomor HP melalui profil, kendala pengguna/sistem

category: Ubah Password
   sub_category: Perubahan Melalui Profil
   DETAIL: cara ubah password melalui profil

category: Ubah Penanggung Jawab
   sub_category: Perubahan Melalui Profil
   DETAIL: cara ubah penanggung jawab, kendala pengguna/sistem

category: Ubah Status Usaha
   sub_category: Perubahan Melalui Profil
   DETAIL: cara ubah status/skala usaha, kendala pengguna/sistem

category: Permohonan Baru
   sub_category: Permohonan Baru
   DETAIL: cara menerbitkan NIB baru, kendala akses halaman permohonan baru, kendala modal disetor/ditempatkan PMA

category: Perubahan
   sub_category: Perubahan
   DETAIL: perubahan data usaha/badan usaha, tambah API, ubah data yang terhubung/tidak dengan AHU, penyesuaian jenis badan usaha (AUM), data tidak bisa diubah, NIB tidak terdaftar di K/L, perubahan nama/jenis badan usaha

category: Pengembangan
   sub_category: Pengembangan
   DETAIL: tambah/hapus bidang usaha, isi formulir data dan alamat usaha, validasi risiko, gagal tambah bidang usaha, hapus KBLI, NIB belum terbit pasca pernyataan mandiri, salah input investasi, kendala lengkapi pernyataan mandiri

category: Perluasan
   sub_category: Perluasan
   DETAIL: cara perluasan kegiatan usaha, kendala sistem

category: Perpanjangan
   sub_category: Perpanjangan
   DETAIL: cara perpanjangan kegiatan usaha, kendala sistem

category: Pencabutan
   sub_category: Pencabutan
   DETAIL: pencabutan NIB, likuidasi, penghapusan KBLI, proses/permintaan/progres dalam atau melewati SLA, masalah sistem dan pengguna

category: Pemenuhan Persyaratan
   sub_category: Pemenuhan Persyaratan
   DETAIL: pemenuhan persyaratan dan dokumen pendukung, masalah sistem OSS/K/L, sertifikat standar KBLI konstruksi

category: Pembatalan
   sub_category: Pembatalan
   DETAIL: cara pembatalan, kendala sistem menu pembatalan

category: Merger
   sub_category: Merger
   DETAIL: cara merger, kendala sistem merger

category: Pencetakan Perizinan Berusaha
   sub_category: Cetak NIB
   DETAIL: cetak NIB dan lampiran, pembaruan data, tampilan KBLI, status izin, versi bahasa Inggris, masalah teknis website/aplikasi OSS
   sub_category: Cetak Produk Perizinan selain NIB
   DETAIL: cetak produk perizinan selain NIB, data tidak lengkap/tidak sesuai, masalah sistem dan pengguna

category: Migrasi
   sub_category: Migrasi Kegiatan Usaha
   DETAIL: informasi migrasi kegiatan usaha
   sub_category: Migrasi Hak Akses
   DETAIL: informasi migrasi hak akses, kendala pengguna

category: Perizinan Berusaha Lainnya
   sub_category: Perizinan Berusaha Lainnya
   DETAIL: kendala dan informasi perizinan usaha dan kewajiban NIB, perizinan sebelum OSS RBA, kegiatan usaha LPG/event, akun AHU terblokir, pengangkatan KKI

category: Perizinan Tunggal
   sub_category: Standar Nasional Indonesia dan Sistem Jaminan Produk Halal
   DETAIL: pengajuan/pemenuhan persyaratan/pencetakan SNI dan Sertifikat Halal, masalah sistem dan pengguna

category: Laporan LKPM
   sub_category: Laporan LKPM
   DETAIL: masalah sistem klik/tampil data LKPM, kesalahan data pelaku usaha, ketidaksesuaian tanggal pelaporan, migrasi KBLI, informasi umum dan klarifikasi teguran LKPM

category: Realisasi Impor
   sub_category: Realisasi Impor
   DETAIL: cara mengajukan laporan realisasi impor

category: Informasi mekanisme pengawasan
   sub_category: Informasi mekanisme pengawasan
   DETAIL: informasi umum pengawasan, tindakan administratif pelaku usaha, sanksi administratif

category: Tax Holiday
   sub_category: Tax Holiday
   DETAIL: informasi pengajuan Tax Holiday

category: Tax Allowance
   sub_category: Tax Allowance
   DETAIL: informasi pengajuan Tax Allowance

category: Investment Allowance
   sub_category: Investment Allowance
   DETAIL: informasi pengajuan Investment Allowance

category: Vokasi
   sub_category: Vokasi
   DETAIL: informasi umum Vokasi

category: Penelitian dan pengembangan
   sub_category: Penelitian dan pengembangan
   DETAIL: informasi umum penelitian dan pengembangan

category: Tax Holiday di KEK
   sub_category: Tax Holiday di KEK
   DETAIL: informasi pengajuan Tax Holiday di KEK

category: Tax Allowance di KEK
   sub_category: Tax Allowance di KEK
   DETAIL: informasi pengajuan Tax Allowance di KEK

category: Masterlist
   sub_category: Masterlist
   DETAIL: informasi pengajuan Masterlist

category: Perizinan Berusaha
   sub_category: Perizinan Berusaha
   DETAIL: progres Perizinan Berusaha berbasis Risiko (dalam/melewati SLA), progres ESDM, progres perpanjangan SIO

category: Perizinan Dasar
   sub_category: Perizinan Dasar
   DETAIL: progres perizinan lingkungan dan PKKPR, status proses dalam/melewati SLA, tahap sebelum keluarnya SPS, verifikasi KKPR 181, perizinan kawasan hutan

category: Pengawasan
   sub_category: Pengawasan
   DETAIL: progres verifikasi LKPM

category: PB UMKU
   sub_category: PB UMKU
   DETAIL: progres PB-UMKU (dalam/melewati SLA)

category: Progres Tiket
   sub_category: Progres Tiket Eskalasi
   DETAIL: progres tiket eskalasi (masih/melewati SLA)

category: Daftar Sanksi LKPM
   sub_category: Daftar Sanksi LKPM
   DETAIL: informasi daftar sanksi LKPM

category: Daftar Sanksi
   sub_category: Daftar Sanksi
   DETAIL: informasi daftar sanksi

category: Contact Center
   sub_category: Contact Center
   DETAIL: informasi umum Contact Center OSS, outbound

category: Tatap Muka
   sub_category: Perizinan Berusaha
   DETAIL: kirim ulang jadwal konsultasi, informasi konsultasi tatap muka, kendala sistem daftar konsultasi (akun terblokir), pembatalan antrian konsultasi
   sub_category: Pengawasan
   DETAIL: kirim ulang jadwal konsultasi virtual pengawasan, follow up konsultasi virtual pengawasan, klinik LKPM
   sub_category: Kepolisian
   DETAIL: kirim ulang jadwal konsultasi kepolisian

category: Sinkronisasi Data AHU
   sub_category: Data AHU
   DETAIL: permintaan sinkronisasi data AHU (solved/unsolved by agent)

category: Akun
   sub_category: Akun K/L/D
   DETAIL: kendala sistem verifikasi perizinan berusaha pada akun K/L/D, permintaan UM OSS oleh DPMPTSP
   sub_category: Jenis Badan Usaha Tidak Sesuai
   DETAIL: cara ubah jenis badan usaha
   SUB: Kesalahan akun
   DETAIL: kendala sistem akun undefined, kendala sistem data tertukar
   sub_category: Kirim ulang username dan password
   DETAIL: kendala sistem tidak terima username/password, permintaan kirim ulang username/password
   sub_category: Migrasi akun
   DETAIL: kendala sistem duplikasi email, gagal migrasi karena perubahan direksi
   sub_category: Pengaktifan akun
   DETAIL: permintaan pengaktifan akun
   sub_category: Penonaktifan akun
   DETAIL: permintaan penonaktifan akun
   sub_category: Penutupan kantor perwakilan
   DETAIL: cara penutupan kantor perwakilan dan BULN

category: Id Izin tidak terdaftar
   sub_category: Id Izin tidak terdaftar
   DETAIL: kendala sistem Id Izin tidak terdaftar dengan sistem K/L

category: Data penanggungjawab pada OSS tidak sesuai dengan data pada sistem K/L
   sub_category: Data penanggungjawab pada OSS tidak sesuai dengan data pada sistem K/L
   DETAIL: kendala data penanggung jawab tidak sesuai dengan sistem K/L

category: Aliran Data ke Sistem K/L
   sub_category: Aliran Data ke Sistem K/L
   DETAIL: gangguan aliran data antar sistem, integrasi OSS dengan sistem K/L (INSW, DJP, AHU, Dukcapil, Kemenkes, Kemenhub, Inatrade)

category: Kemitraan
   sub_category: Informasi umum fitur kemitraan
   DETAIL: informasi umum fitur kemitraan

category: KKPR
   sub_category: KKPR
   DETAIL: peta dan perizinan ruang (KKPR/RDTR), masalah unggah polygon, pengecekan RDTR, integrasi sistem, data migrasi, konfirmasi dokumen pendukung, penolakan dan ketidaktampilan SPS

category: Bangunan Gedung
   sub_category: Bangunan Gedung
   DETAIL: informasi PBG dan SLF

category: Persetujuan Lingkungan
   sub_category: Persetujuan Lingkungan
   DETAIL: informasi perizinan lingkungan

category: Sistem Pelayanan Informasi
   sub_category: Klasifikasi Baku Lapangan Usaha Indonesia (2020)
   DETAIL: informasi KBLI dan tingkat risiko usaha, pemilihan KBLI tepat, penggabungan, status penutupan, KBLI tanpa pengampu, KBLI tidak menghasilkan NIB, kategori KBLI single purpose
   sub_category: Bidang Usaha Penanaman Modal (BUPM)
   DETAIL: informasi KBLI dialokasikan untuk UMKM/Koperasi atau terbuka untuk usaha besar/asing
   sub_category: Informasi Lokasi Usaha
   DETAIL: informasi lokasi usaha
   sub_category: Frequently Asked Question
   DETAIL: informasi FAQ
   sub_category: Cek NIB
   DETAIL: cara cek NIB via fitur cari NIB
   sub_category: Pengaduan Masyarakat
   DETAIL: pengaduan masyarakat

category: Regulasi
   sub_category: Perizinan Berusaha
   DETAIL: aturan Angka Pengenal Impor, kantor perwakilan, PP 28/2025, masa berlaku NIB dan izin lainnya, ketentuan KDMP/KMP, format cetakan NIB perorangan, skala usaha berdasarkan modal
   sub_category: PMA
   DETAIL: informasi Grand Father Clause, permodalan dan nilai investasi
   sub_category: PMDN
   DETAIL: informasi PMDN
   sub_category: Regulasi Lainnya
   DETAIL: informasi regulasi kementerian/lembaga lain

category: Kendala Sistem
   sub_category: Sistem OSS
   DETAIL: kegagalan terbit izin, hilangnya ID izin, duplikasi NPWP/NIB, perbaikan substansi pada SPI
   sub_category: Sistem K/L
   DETAIL: kendala sistem K/L

category: Rekomendasi Alih Status
   SUB: Rekomendasi Alih Status
   DETAIL: informasi rekomendasi alih status

category: Kode Verifikasi (OTP)
   sub_category: Kode Verifikasi (OTP)
   DETAIL: kendala kode verifikasi akun, kegagalan input oleh pengguna, kode verifikasi email/nomor tidak terkirim akibat bug sistem

category: Progres surat
   sub_category: Progres surat
   DETAIL: progres surat LOI dan Grand Father Clause ke Deregulasi, progres surat lainnya

category: SPAM / Auto Reply / Iseng / Emoticon / Feedback
   sub_category: SPAM / Auto Reply / Iseng / Emoticon / Feedback
   DETAIL: SPAM/Auto Reply/Iseng/Emoticon/Feedback

category: Pertanyaan di luar OSS
   sub_category: Pertanyaan di luar OSS
   DETAIL: pertanyaan di luar OSS


EXAMPLES:
Q: "Bagaimana cara mengubah email di OSS?"
A: {"category": "Ubah Email atau Nomor Ponsel", "sub_category": "Perubahan Email tanpa Log in"}

Q: "Saya lupa password OSS"
A: {"category": "Reset Password", "sub_category": "Reset Password"}

Q: "Cara membuat NIB baru?"
A: {"category": "Permohonan Baru", "sub_category": "Permohonan Baru"}

Q: "Apa itu blockchain?"
A: {"category": "Pertanyaan di luar OSS", "sub_category": "Pertanyaan di luar OSS"}

Now classify this question using ONLY the categories listed above:"""

    user = f"""Question: {user_query}

Remember: Output ONLY the JSON object, use EXACT category names from the list."""

    payload = {
        "model": os.getenv('LLM_MODEL'),
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user}
        ],
        "format": "json", 
        "stream": False,
        "temperature": 0.1  
    }
    
    try:
        response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        content = data.get("message", {}).get("content", "").strip()
        
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```\s*', '', content)
        content = content.strip()
        
        json_match = re.search(r'\{[^{}]*"category"[^{}]*"sub_category"[^{}]*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
        
        result = json.loads(content)
        
        if "category" not in result or "sub_category" not in result:
            raise ValueError("Missing required keys")
        
        print(f"Classification result: {result}")
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Raw content: {content}")
        return {"category": "Unknown", "sub_category": "Unknown"} 
    except Exception as e:
        print(f"Error in classification: {e}")
        return {"category": "Unknown", "sub_category": "Unknown"} 