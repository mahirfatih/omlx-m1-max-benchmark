# oMLX · M1 Max · Yerel LLM Benchmark

> Apple **M1 Max (64 GB)** üzerinde [oMLX](https://omlx.ai) ile çalışan **6 yerel LLM**'in
> token hızı, model boyutları, profil ayarları ve **uncensored / heretic** sınıflandırması.

[![Platform](https://img.shields.io/badge/platform-Apple%20Silicon%20(arm64)-000?logo=apple&logoColor=white)](#donanım--yazılım)
[![oMLX](https://img.shields.io/badge/oMLX-0.7.3-blue)](https://omlx.ai)
[![macOS](https://img.shields.io/badge/macOS-26.7.2-lightgrey)](#donanım--yazılım)
[![Models](https://img.shields.io/badge/models-6-purple)](#modeller)
[![Security](https://img.shields.io/badge/security-red--team-red)](docs/security/README.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[English](README.md) · **Türkçe**

---

## Genel bakış

Bu depo, **Apple M1 Max + 64 GB** üzerinde tamamen cihaz içinde, **oMLX**
(MLX tabanlı, OpenAI uyumlu bir sunucu) ile çalışan **6 yerel LLM**'in
tekrarlanabilir bir benchmark'ını belgeler.

İçerdikleri:

- İngilizce ve Türkçe için **decode hızı** (tok/s), her dil iki kez.
- **Model boyutları** ve parametre sayıları.
- Kaynak kanıtlı **uncensored / heretic / abliterated** sınıflandırması.
- RAM'i sabit tutan **ayarlı oMLX profilleri** (OOM yok, GPU takılması yok).
- **Güvenlik katmanı**: sunucu denetimi ve model red-team yetenek benchmark'ı.
- **Depo analizi**: modellerin gerçek bir projeyi ne kadar sürede ve ne kadar doğru analiz ettiği.
- **Çoğaltma script'leri** (benchmark + çok dilli kod doğrulama).

Depo yapısı, gerçek ve yayınlanmış bir referans projeyi birebir yansıtır:
[`mahirfatih/net-traffic-control-catalog`](https://github.com/mahirfatih/net-traffic-control-catalog).
Benchmark'lardan biri modellere bu projeyi doğrudan analiz ettirir
([Depo analizi](#depo-analizi)).

> Tüm sayılar [Donanım & Yazılım](#donanım--yazılım) bölümündeki makinede ölçüldü.
> Sonuçlar prompt uzunluğuna, nicelemeye ve arka plan yüküne göre değişir.

## İçindekiler

- [Donanım & Yazılım](#donanım--yazılım)
- [Modeller](#modeller)
- [Benchmark sonuçları](#benchmark-sonuçları)
- [Uncensored / Heretic sınıflandırması](#uncensored--heretic-sınıflandırması)
- [Profiller](#profiller)
- [Güvenlik](#güvenlik)
- [Depo analizi](#depo-analizi)
- [Kod benchmark'ı](#kod-benchmarkı)
- [Halüsinasyon ve hata riski](#halüsinasyon-ve-hata-riski)
- [Çoğaltma](#çoğaltma)
- [Depo yapısı](#depo-yapısı)
- [Lisans](#lisans)

---

## Donanım & Yazılım

| Öğe | Değer |
|---|---|
| Makine | **Apple M1 Max** (10 çekirdek CPU: 8P + 2E, 32 çekirdek GPU) |
| Bellek | **64 GB** birleşik |
| İşletim sistemi | **macOS 26.7.2** (25G332), arm64 |
| Sunucu | **oMLX 0.7.3** — `http://127.0.0.1:8000/v1` |
| Çıkarım | MLX, **4-bit** ağırlık, **4-bit KV cache** (turboquant) |
| Yükleme | Tembel, aynı anda tek model, 180 s boşta boşaltma |
| Bellek koruması | tier `aggressive`, soft `0.85`, hard `0.95` |

- oMLX sitesi: <https://omlx.ai>
- oMLX kaynağı: <https://github.com/jundot/omlx> (Apache 2.0)

## Modeller

| Model | Parametre | Disk | Kaynak |
|---|---|---:|---|
| `Qwen3-Coder-30B-A3B-Instruct-4bit` | 30B MoE (~3B aktif) | 16 GB | [HF](https://huggingface.co/mlx-community/Qwen3-Coder-30B-A3B-Instruct-4bit) |
| `Qwen3.6-35B-A3B-4bit` | 35B MoE (~3B aktif) | 19 GB | [HF](https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-4bit) |
| `Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit` | 35B MoE, abliterated | 19 GB | [HF](https://huggingface.co/froggeric/Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit) |
| `Ornith-1.5-35B-A3B-MLX-4bit` | 35B MoE | 18 GB | [HF](https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B-MLX-4bit) |
| `gemma-4-26B-A4B-it-heretic-4bit` | 26B MoE, abliterated | 15 GB | [HF](https://huggingface.co/mlx-community/gemma-4-26B-A4B-it-heretic-4bit) |
| `Qwen3.8-27B-Uncensored-MLX` | 27B dense, abliterated | 15 GB | [HF](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-MLX) |

**Disk toplamı:** ~102 GB · **Çalışma zamanı:** model başına ~17–20 GB.

## Benchmark sonuçları

**Yöntem:** her model boşaltılır, istek üzerine yüklenir (ısınma), sonra aynı
İngilizce ve Türkçe prompt iki kez sorulur. Hız = `completion_tokens / geçen süre`.
Ayarlar: `ctx 32768`, `temp 0.2`, `max_tokens 220`, thinking kapalı.

| # | Model | Profil | EN tok/s | TR tok/s | **Ortalama** | Yükleme (s) |
|---|---|---|---:|---:|---:|---:|
| 🥇 | `Qwen3.6-35B-A3B-4bit` | `qwen3` | 72.2 | 74.7 | **73.4** | 8.9 |
| 🥈 | `Qwen3.6-35B-A3B-Uncensored-Heretic` | `qwen36-heretic` | 69.2 | 73.0 | **71.1** | 8.4 |
| 🥉 | `Ornith-1.5-35B-A3B` | `qwen3` | 60.0 | 60.4 | **60.2** | 6.5 |
| 4 | `gemma-4-26B-A4B-it-heretic` | `gemma4-heretic` | 59.5 | 60.7 | **60.1** | 9.0 |
| 5 | `Qwen3-Coder-30B-A3B-Instruct` | `qwen3` | 43.4 | 41.8 | **42.6** | 4.7 |
| 6 | `Qwen3.8-27B-Uncensored` | `qwen36-heretic` | 18.3 | 18.1 | **18.2** | 6.6 |

Tam tablo, grafikler ve ham rapor: [`docs/reference/RESULTS.md`](docs/reference/RESULTS.md).

## Uncensored / Heretic sınıflandırması

> **Heretic** (`p-e-w/heretic`) abliterasyon yapan bir *araç/yöntemdir*;
> **Uncensored** ise *sonuçtur*. Her Heretic model abliterated'dır, ama her
> abliterated model Heretic aracıyla yapılmamış olabilir.

| Model | Tür | Uncensored | Heretic / abliterated |
|---|---|:---:|:---:|
| Qwen3-Coder-30B | standart | ❌ | ❌ |
| Qwen3.6-35B | standart | ❌ | ❌ |
| Ornith-1.5-35B | standart | ❌ | ❌ |
| **gemma-4-26B-Heretic** | heretic + uncensored | ✅ | ✅ |
| **Qwen3.6-35B-Heretic** | uncensored + heretic | ✅ | ✅ |
| **Qwen3.8-27B-Uncensored** | uncensored + abliterated | ✅ | ✅ |

Kanıtlar, HF alıntıları ve yerel davranış testleri:
[`docs/reference/MODELS.md`](docs/reference/MODELS.md).

## Profiller

| Ayar | `qwen3` | `qwen36-heretic` | `gemma4-heretic` |
|---|---:|---:|---:|
| Context | 32768 | 32768 | 32768 |
| Max tokens | **4096** | 2048 | 2048 |
| Temperature | 0.2 | 0.2 | 0.2 |
| Top-p / Top-k | 0.95 / 20 | 0.95 / 20 | 0.95 / 20 |
| Repetition penalty | 1.1 | 1.1 | 1.1 |
| Min-p / Presence | 0.05 / 0.3 | 0.05 / 0.3 | 0.05 / 0.3 |
| Thinking | kapalı | kapalı | kapalı |
| KV cache 4-bit | ✅ | ✅ | ✅ |

Tam ayarlar: [`docs/reference/PROFILES.md`](docs/reference/PROFILES.md).

## Güvenlik

İki katman, ikisi de yerel ve yetkili kullanım için:

- **Sunucu denetimi** — [`scripts/security/security-probe.py`](scripts/security/security-probe.py):
  loopback bind, LAN açığı, `/v1` ve admin auth, auth'suz OpenAPI, wildcard CORS;
  `--model` ile prompt injection / jailbreak direnci.
- **Red-team yetenek benchmark'ı** — [`scripts/security/redteam-benchmark.py`](scripts/security/redteam-benchmark.py):
  yerel, kasıtlı olarak zafiyetli bir lab'a karşı exploit üretimi + tersine
  mühendislik.

Bulgular ve tehdit modeli: [`docs/security/README.md`](docs/security/README.md).
Sonuç tablosu: [`docs/security/OFFENSIVE-BENCHMARK.md`](docs/security/OFFENSIVE-BENCHMARK.md).

> Bu araçlar **yalnızca kendi makinene** karşı çalışır. Probe, loopback olmayan
> hedefi reddeder; lab sadece `127.0.0.1` dinler. Üçüncü taraf sistemlere
> yöneltmek yasadışıdır ve bu araçların amacı değildir.

## Depo analizi

İkinci bir yetenek benchmark'ı: her modelin gerçek bir depoyu nasıl analiz ettiği.
Hedef: [`mahirfatih/net-traffic-control-catalog`](https://github.com/mahirfatih/net-traffic-control-catalog)
— 6.731 host, 27 kategori ve 22 servis içeren, yayınlanmış CC0 bir katalog. Her
modele aynı özet (dosya ağacı, README, veri istatistikleri) ve aynı görev verilir;
puan, cevabın deponun kendi gerçeklerinden kaç tanesini andığıdır.

| Model | Cevap (s) | tok/s | Bulunan gerçek | Puan |
| :--- | ---: | ---: | ---: | ---: |
| `Ornith-1.5-35B-A3B` | 6.8 | 53.5 | 10/12 | **83%** |
| `Qwen3-Coder-30B-A3B-Instruct` | 6.6 | 35.8 | 7/12 | **58%** |
| `Qwen3.6-35B-A3B` | 4.8 | 62.6 | 6/12 | **50%** |
| `Qwen3.6-35B-A3B-Uncensored-Heretic` | 4.7 | 57.8 | 5/12 | **42%** |
| `gemma-4-26B-A4B-it-heretic` | 4.3 | 38.6 | 4/12 | **33%** |
| `Qwen3.8-27B-Uncensored-MLX` | 46.1 | 15.2 | 0/12 | **0%** |

**En hızlı cevap en iyisi değildi.** Ornith-1.5 gerçek sayıları andı; Qwen3.6-35B
%30 daha hızlı cevaplayıp yarısı kadar gerçek buldu. İki model olmayan bir dosya
sayısı **uydurdu** (`scripts/` için "6.863 dosya"; gerçek: **136**). En yavaş
model hiç cevap vermedi.

Tam analiz: [`docs/analysis/net-traffic-control-catalog.md`](docs/analysis/net-traffic-control-catalog.md).

## Kod benchmark'ı

Üçüncü yetenek benchmark'ı ve en katı olanı: modelin kodu **çalıştırılır**, sadece
okunmaz. Her modelden beş problem için Python çözümü istenir
([`problems/`](problems/README.md), 56 gizli vaka) ve kod, 20 saniyelik zaman
aşımı altında bu vakalara karşı çalıştırılır.

| Model | p01 | p02 | p03 | p04 | p05 | Toplam |
| :--- | :---: | :---: | :---: | :---: | :---: | ---: |
| `Qwen3.6-35B-A3B` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `Qwen3.6-35B-A3B-Uncensored-Heretic` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `Ornith-1.5-35B-A3B` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `gemma-4-26B-A4B-it-heretic` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `Qwen3-Coder-30B-A3B-Instruct` | 12/12 | 10/10 | ❌ sözdizimi | 12/12 | 11/12 | **45/46** |
| `Qwen3.8-27B-Uncensored-MLX` | 12/12 | 10/10 | ❌ tanımsız | 12/12 | ❌ tanımsız | **34/34** |

**Dört model her şeyi çözdü.** Hatalar somut: Qwen3-Coder bir `else` sonrası
geçersiz girinti üretti (modül içe aktarılamıyor); Qwen3.8 iki problemde istenen
fonksiyon adını hiç tanımlamadı. Toplamı 56'nın altında olan satırlar, modelin
kodunun *yüklenemediği* problemlerdir; hiç vaka çalışmadığı için kesin sıfırdır.

Tam analiz: [`docs/analysis/code-benchmark.md`](docs/analysis/code-benchmark.md).

## Halüsinasyon ve hata riski

Bir model var olmayan API'leri uyduruyor mu? 102 dilin her biri, gerçek bir
dokümante API ile **uydurma bir eşi** (`functools.reducex`, `{#eachx}`) üzerinden
yoklanır ve modelin hangisinin gerçek olduğunu söylemesi istenir.

| Model | Halüsinasyon (uydurma → "gerçek") | Yanlış alarm (gerçek → "uydurma") | Brier ↓ |
| :--- | ---: | ---: | ---: |
| `Qwen3.6-35B-A3B` | **0%** (0/102) | 0% (0/102) | 0.001 |
| `Qwen3.6-35B-A3B-Uncensored-Heretic` | **0%** (0/102) | 0% (0/102) | 0.001 |
| `Ornith-1.5-35B-A3B` | **0%** (0/102) | 2% (2/102) | 0.009 |
| `gemma-4-26B-A4B-it-heretic` | **0%** (0/102) | 0% (0/102) | 0.0 |
| `Qwen3-Coder-30B-A3B-Instruct` | **0%** (0/91) | 2% (2/91) | 0.006 |

**Hiçbir model API uydurmadı.** Modellerin kaçırdığı yerlerde hata, gerçek bir
API'ye "uydurma" demek yönünde — yani güvenli tarafta. `Qwen3.8-27B-Uncensored`
tabloda yok, bilerek: üç denemede **~5,2 saat** GPU zamanı harcayıp diğerlerinin
1–2 dakikada bitirdiği korpüsü yine de tamamlayamadı.

Tam analiz: [`docs/analysis/hallucination.md`](docs/analysis/hallucination.md).

## Çoğaltma

1. [oMLX](https://omlx.ai)'i kur ve başlat (`127.0.0.1:8000`, OpenAI uyumlu).
2. [Modeller](#modeller) listesindeki modelleri indir.
3. Profilleri uygula ([`profiles/omlx-profiles.json`](profiles/omlx-profiles.json)):

```bash
python3 scripts/config/apply-profiles.py --apply
```

1. Benchmark'ı çalıştır:

```bash
python3 scripts/measure/benchmark.py
python3 scripts/measure/code-matrix-test.py
python3 scripts/measure/repo-analysis-test.py --repo ~/Sites/net-traffic-control-catalog
python3 scripts/measure/code-benchmark.py --selftest   # model gerekmez
python3 scripts/measure/code-benchmark.py --models Qwen3.6-35B-A3B-4bit:qwen3
```

Ayrıntılı adımlar: [`docs/guides/REPRODUCING.md`](docs/guides/REPRODUCING.md).

## Depo yapısı

```text
omlx-m1-max-benchmark/
├── README.md / README.tr.md
├── docs/
│   ├── overview/     ne ölçüldü
│   ├── guides/       yöntem, çoğaltma, model seçimi
│   ├── reference/    modeller, profiller, sonuçlar
│   ├── security/     tehdit modeli + red-team
│   ├── testing/      ne nasıl doğrulanır
│   └── diagrams/     etkileşimli mimari diyagramı
├── benchmarks/       ham rapor
├── profiles/         sanitize edilmiş oMLX profilleri
├── config/           örnek global ayarlar
└── scripts/          ölçüm + güvenlik araçları
```

## Lisans

[MIT](LICENSE). Model ağırlıkları **dahil değildir** ve kendi lisanslarını korur.
