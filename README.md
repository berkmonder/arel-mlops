# 🚀 Arel MLOps Projesi

Bu repo, eğitim amaçlı olup; Veri üretiminden, makine öğrenmesi modellerinin geliştirilmesi, takibi ve operasyonel süreçlerini (MLOps) yönetmek için tasarlanmış, uçtan uca basit bir boru hattı (pipeline) örneğini içermektedir.

## 📂 Proje Yapısı

```bash
arel-mlops/
├── notebooks/
│   └── 1.0-demo.py
├── presentation/
├── src/                # Temel kaynak kodlar
│   ├── data_gen.py     # Veri üretici
│   ├── pipeline.py     # Prefect Akışı (GMM + Isolation Forest)
│   └── dashboard.py    # Streamlit (Canlı Takip & Drift)
├── docker-compose.yaml
├── Dockerfile
├── pyproject.toml
├── README.md
└── uv.lock
```

## 🐳 Docker ile Çalıştırma:

```bash
# docker-compose.yaml dosyasındaki tüm servisleri ayağa kaldırır
docker compose up -d

# Servisleri durdurmak için
docker compose down
```
