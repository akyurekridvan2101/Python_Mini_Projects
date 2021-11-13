import random

def kelime_sec():
    kelimeler = ["python", "programlama", "kodlama", "oyun", "merhaba", "selam"]
    return random.choice(kelimeler)

def kelimeyi_goster(gizli_kelime, tahmin_edilen_harfler):
    goruntulenmis_kelime = ""
    for harf in gizli_kelime:
        if harf in tahmin_edilen_harfler:
            goruntulenmis_kelime += harf
        else:
            goruntulenmis_kelime += "_"
    return goruntulenmis_kelime

def kelime_oyunu():
    gizli_kelime = kelime_sec()
    tahmin_edilen_harfler = []
    hak = 6

    print("Hoş geldiniz! Kelimeyi tahmin edin.")
    print(kelimeyi_goster(gizli_kelime, tahmin_edilen_harfler))

    while hak > 0:
        tahmin = input("Bir harf tahmin edin: ").lower()

        if tahmin.isalpha() and len(tahmin) == 1:
            if tahmin in tahmin_edilen_harfler:
                print("Bu harfi zaten tahmin ettiniz. Tekrar deneyin.")
            elif tahmin in gizli_kelime:
                tahmin_edilen_harfler.append(tahmin)
                print("Doğru tahmin! Kelime şu şekilde görünüyor:")
                print(kelimeyi_goster(gizli_kelime, tahmin_edilen_harfler))
            else:
                hak -= 1
                print("Yanlış tahmin. Kalan hakkınız:", hak)
        else:
            print("Geçerli bir harf girişi yapın.")

        if "_" not in kelimeyi_goster(gizli_kelime, tahmin_edilen_harfler):
            print("Tebrikler! Kelimeyi doğru tahmin ettiniz: {}".format(gizli_kelime))
            break

    if hak == 0:
        print("Üzgünüm, hakkınız bitti. Doğru kelime: {}".format(gizli_kelime))

if __name__ == "__main__":
    kelime_oyunu()
