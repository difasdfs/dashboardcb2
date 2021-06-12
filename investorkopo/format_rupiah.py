def main(angka, total_penjualan = False):

    angka = int(angka)

    if angka >= 1_000_000_000:
        milyaran = angka // 1_000_000_000
        angka = angka - (milyaran*1_000_000_000)
        ratusan_juta = angka // 100_000_000
        angka = angka - (ratusan_juta*100_000_000)
        puluhan_juta = angka // 10_000_000
        angka = angka - (puluhan_juta*10_000_000)
        juta = angka // 1_000_000
        angka = angka - (juta*1_000_000)
        ratusan_ribu = angka // 100_000
        angka = angka - (ratusan_ribu*100_000)
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)   

        # print("milyaran rupiah")
        if total_penjualan:
            hasil = "Rp " + str(milyaran) + "." + str(ratusan_juta) + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            return hasil[:7] + "m"
        else:
            return "Rp " + str(milyaran) + "." + str(ratusan_juta) + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
        
    elif angka >= 100_000_000:
        ratusan_juta = angka // 100_000_000
        angka = angka - (ratusan_juta*100_000_000)
        puluhan_juta = angka // 10_000_000
        angka = angka - (puluhan_juta*10_000_000)
        juta = angka // 1_000_000
        angka = angka - (juta*1_000_000)
        ratusan_ribu = angka // 100_000
        angka = angka - (ratusan_ribu*100_000)
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)

        # print("jutaan rupiah")
        if total_penjualan:
            hasil = "Rp " + str(ratusan_juta) + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            return hasil[:9] + "jt"
        else:
            return "Rp " + str(ratusan_juta) + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
        
    elif angka >= 10_000_000:    
        puluhan_juta = angka // 10_000_000
        angka = angka - (puluhan_juta*10_000_000)
        juta = angka // 1_000_000
        angka = angka - (juta*1_000_000)
        ratusan_ribu = angka // 100_000
        angka = angka - (ratusan_ribu*100_000)
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)

        # print("puluhan juta rupiah")
        if total_penjualan:
            hasil = "Rp " + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            return hasil[:7] + "jt"
        else:
            return "Rp " + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
    
    elif angka >= 1_000_000:

        juta = angka // 1_000_000
        angka = angka - (juta*1_000_000)
        ratusan_ribu = angka // 100_000
        angka = angka - (ratusan_ribu*100_000)
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        if total_penjualan:
            hasil = "Rp " + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            return hasil[:6] + "jt"
        else:
            return "Rp " + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
    elif angka >= 100_000:
        ratusan_ribu = angka // 100_000
        angka = angka - (ratusan_ribu*100_000)
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        # print("ratusan ribu rupiah")
        if total_penjualan:
            hasil = "Rp " + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            return hasil[:8] + "rb"
        else:
            return "Rp " + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
    elif angka >= 10_000:
        
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        # print("puluhan ribu rupiah")
        if total_penjualan:
            hasil = "Rp " + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            return hasil[:7] + "rb"
        else:
            return "Rp " + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
    elif angka >= 1_000:
        
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        # print("ribuan rupiah")
        if total_penjualan:
            hasil = "Rp " + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            return hasil[:6] + "rb"
        else:
            return "Rp " + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)

    elif angka >= 100:
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        # print("ribuan rupiah")
        return "Rp " + str(ratusan) + str(puluhan) + str(angka)

    elif angka >= 10:
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        # print("ribuan rupiah")
        return "Rp " + str(puluhan) + str(angka)

    else:
        # print("satuan rupiah")
        return "Rp " + str(angka)
