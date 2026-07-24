# CRG + OpenCode Workflow

Panduan menjalankan **Code Review Graph (CRG)** dan **OpenCode** setelah komputer/laptop direstart.

---

## 1. Struktur Instalasi

CRG menggunakan Python Virtual Environment:

```text
C:\CRG\.venv\
```

CRG:

```text
C:\CRG\.venv\Scripts\code-review-graph.exe
```

Python:

```text
C:\CRG\.venv\Scripts\python.exe
```

Project:

```text
C:\Users\User\Desktop\project\...
```

Konfigurasi MCP OpenCode:

```text
C:\Users\User\Desktop\project\...\opencode.jsonc
```

Plugin CRG OpenCode:

```text
C:\Users\User\.config\opencode\plugins\crg-plugin.ts
```

---

# 2. Setelah Restart Laptop

Setiap kali laptop selesai restart, buka **Command Prompt (CMD)**.

Aktifkan Virtual Environment CRG:

```cmd
C:\CRG\.venv\Scripts\activate.bat
```

Jika berhasil, prompt akan berubah menjadi:

```text
(.venv) C:\...
```

Contoh:

```text
(.venv) C:\CRG>
```

---

# 3. Masuk ke Project

Jalankan:

```cmd
cd /d C:\Users\User\Desktop\project\...
```

Prompt akan menjadi:

```text
(.venv) C:\Users\User\Desktop\project\...>
```

---

# 4. Cek Instalasi CRG

Pastikan CRG yang digunakan berasal dari Virtual Environment.

Jalankan:

```cmd
where code-review-graph
```

Hasil yang diharapkan:

```text
C:\CRG\.venv\Scripts\code-review-graph.exe
```

Jika ada hasil kedua seperti:

```text
C:\Users\User\AppData\Roaming\Python\Python314\Scripts\code-review-graph.exe
```

tidak masalah.

Yang penting:

```text
C:\CRG\.venv\Scripts\code-review-graph.exe
```

berada di urutan pertama.

---

# 5. Cek Versi CRG

Jalankan:

```cmd
code-review-graph --version
```

Hasil yang diharapkan:

```text
code-review-graph 2.3.7
```

---

# 6. Cek Status Knowledge Graph

Jalankan:

```cmd
code-review-graph status
```

Contoh hasil:

```text
Nodes: 58
Edges: 408
Files: 17
Languages: javascript, typescript
```

Jika graph masih berisi data dan tidak ada perubahan kode, **tidak perlu melakukan build ulang**.

Langsung jalankan OpenCode:

```cmd
opencode
```

---

# 7. Jika Ada Perubahan Kode

Jika kamu telah mengubah kode project sejak terakhir kali CRG melakukan build, gunakan:

```cmd
code-review-graph update
```

Perintah ini melakukan incremental update dan hanya memproses file yang berubah.

Setelah selesai, cek status:

```cmd
code-review-graph status
```

Kemudian jalankan OpenCode:

```cmd
opencode
```

---

# 8. Jika Graph Bermasalah

Jika terjadi masalah pada graph atau hasil `status` tidak sesuai, lakukan full rebuild:

```cmd
code-review-graph build
```

Setelah selesai, cek:

```cmd
code-review-graph status
```

Hasil yang diharapkan adalah jumlah `Nodes` dan `Edges` lebih dari 0.

Contoh:

```text
Nodes: 58
Edges: 408
Files: 17
Languages: javascript, typescript
```

Kemudian jalankan:

```cmd
opencode
```

---

# 9. Konfigurasi MCP CRG

Project menggunakan konfigurasi:

```text
C:\Users\User\Desktop\project\...\opencode.jsonc
```

Konfigurasi MCP CRG harus menggunakan Python dari Virtual Environment:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "code-review-graph": {
      "type": "local",
      "command": [
        "C:\\CRG\\.venv\\Scripts\\python.exe",
        "-m",
        "code_review_graph",
        "serve",
        "--repo",
        "C:\\Users\\User\\Desktop\\project\\..."
      ]
    }
  }
}
```

Jangan mengubah:

```text
C:\CRG\.venv\Scripts\python.exe
```

menjadi:

```text
C:\Python314\python.exe
```

Karena CRG dan dependency Tree-sitter yang digunakan oleh MCP berada di Virtual Environment:

```text
C:\CRG\.venv\
```

---

# 10. Menjalankan OpenCode

Setelah Virtual Environment aktif dan berada di folder project:

```cmd
C:\CRG\.venv\Scripts\activate.bat
cd /d C:\Users\User\Desktop\project\...
opencode
```

OpenCode akan membaca konfigurasi project:

```text
opencode.jsonc
```

dan menjalankan CRG MCP melalui:

```text
C:\CRG\.venv\Scripts\python.exe
```

---

# 11. Mengecek MCP CRG di OpenCode

Setelah OpenCode berjalan, periksa status MCP.

Cari:

```text
code-review-graph
```

Status yang diharapkan:

```text
enabled
```

atau:

```text
connected
```

Jika status:

```text
disabled
```

periksa kembali konfigurasi:

```text
opencode.jsonc
```

Pastikan path Python menggunakan:

```text
C:\\CRG\\.venv\\Scripts\\python.exe
```

---

# 12. Test CRG di OpenCode

Setelah MCP CRG aktif, gunakan prompt berikut untuk menguji CRG.

## Test 1 — Architecture

```text
Use the code-review-graph MCP tools to analyze the architecture of this repository.

Please:
1. Identify the main components.
2. Identify the relationships between components.
3. Identify the most important dependencies.
4. Give me an architecture overview based specifically on the code-review-graph data.

Do not rely only on manually reading files. Use the code-review-graph MCP tools.
```

---

## Test 2 — Search

```text
Use code-review-graph to search for the main components or functions related to the portfolio homepage.

Show me the relevant nodes found in the graph and explain their relationships.
```

---

## Test 3 — Impact Analysis

```text
Use the code-review-graph MCP tools to analyze the impact of changing the main layout component of this Astro project.

Identify:
- Files that may be affected
- Components that depend on it
- Functions or modules connected to it
- Potential risks of making the change

Use the graph's impact analysis rather than guessing from the file structure.
```

---

## Test 4 — Dead Code

```text
Use code-review-graph to find potential dead code in this repository.

List the functions or classes that have no callers or test references, and explain which ones are likely safe or unsafe to remove.
```

---

## Test 5 — Large Functions

```text
Use code-review-graph to identify large or potentially problematic functions in this project.

Show me the largest functions and suggest which ones would benefit most from refactoring.
```

---

# 13. Workflow Harian

## Kondisi A — Tidak Ada Perubahan Kode

Gunakan:

```cmd
C:\CRG\.venv\Scripts\activate.bat
cd /d C:\Users\User\Desktop\project\...
code-review-graph status
opencode
```

Alurnya:

```text
Restart Laptop
      ↓
Aktifkan .venv
      ↓
Masuk Project
      ↓
Cek Status CRG
      ↓
Jalankan OpenCode
```

---

## Kondisi B — Ada Perubahan Kode

Gunakan:

```cmd
C:\CRG\.venv\Scripts\activate.bat
cd /d C:\Users\User\Desktop\project\...
code-review-graph update
code-review-graph status
opencode
```

Alurnya:

```text
Restart Laptop
      ↓
Aktifkan .venv
      ↓
Masuk Project
      ↓
CRG Update
      ↓
Cek Status
      ↓
Jalankan OpenCode
```

---

## Kondisi C — Graph Bermasalah

Gunakan:

```cmd
C:\CRG\.venv\Scripts\activate.bat
cd /d C:\Users\User\Desktop\project\...
code-review-graph build
code-review-graph status
opencode
```

Alurnya:

```text
Restart Laptop
      ↓
Aktifkan .venv
      ↓
Masuk Project
      ↓
Full CRG Build
      ↓
Cek Status
      ↓
Jalankan OpenCode
```

---

# 14. Perintah Penting

| Tujuan             | Perintah                                  |
| ------------------ | ----------------------------------------- |
| Aktifkan CRG venv  | `C:\CRG\.venv\Scripts\activate.bat`       |
| Masuk project      | `cd /d C:\Users\User\Desktop\project\...` |
| Cek lokasi CRG     | `where code-review-graph`                 |
| Cek versi CRG      | `code-review-graph --version`             |
| Cek graph          | `code-review-graph status`                |
| Update incremental | `code-review-graph update`                |
| Full rebuild       | `code-review-graph build`                 |
| Jalankan OpenCode  | `opencode`                                |

---

# 15. Catatan Penting

### Jangan install ulang CRG setiap restart

Tidak perlu menjalankan:

```cmd
pip install code-review-graph
```

setiap kali laptop dinyalakan.

CRG sudah terinstall di:

```text
C:\CRG\.venv\
```

---

### Jangan menjalankan `code-review-graph install` setiap restart

Perintah:

```cmd
code-review-graph install --platform opencode
```

hanya diperlukan saat konfigurasi integrasi awal atau ketika konfigurasi MCP memang perlu dibuat ulang.

---

### Jangan mengubah konfigurasi 9Router

CRG hanya berfungsi sebagai MCP/tool untuk memberikan informasi mengenai struktur kode kepada OpenCode.

Konfigurasi 9Router tetap digunakan untuk routing model AI.

Arsitektur:

```text
                    OpenCode
                       │
            ┌──────────┴──────────┐
            │                     │
            ▼                     ▼
         9Router                CRG MCP
            │                     │
            ▼                     ▼
       AI Provider          Code Knowledge Graph
                                  │
                                  ▼
                         58 Nodes / 408 Edges
                                  │
                                  ▼
                          Project Repository
```

---

# 16. Quick Start

Jika hanya ingin menjalankan semuanya setelah restart:

```cmd
C:\CRG\.venv\Scripts\activate.bat
cd /d C:\Users\User\Desktop\project\...
code-review-graph status
opencode
```

Jika ada perubahan kode:

```cmd
C:\CRG\.venv\Scripts\activate.bat
cd /d C:\Users\User\Desktop\project\...
code-review-graph update
opencode
```

Jika graph bermasalah:

```cmd
C:\CRG\.venv\Scripts\activate.bat
cd /d C:\Users\User\Desktop\project\...
code-review-graph build
opencode
```

---

## Current CRG Status

Project:

```text
...
```

CRG Version:

```text
2.3.7
```

Python Environment:

```text
C:\CRG\.venv
```

Graph:

```text
58 Nodes
408 Edges
17 Files
```

Languages Detected:

```text
JavaScript
TypeScript
```

MCP Configuration:

```text
Project-level OpenCode MCP
```

AI Routing:

```text
9Router
```
