from bs4 import BeautifulSoup
import requests

def ekstraksi_data():
    try:
        req = requests.get('https://www.bmkg.go.id/')
    except Exception:
        return None

    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        
        tanggal = soup.find('span',{'class':'waktu'}).text.split(', ')
        
        result = soup.find('div',{'class':'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
                
        i = 0
        magnitudo = None
        kedalaman = None
        koordinat = None
        lokasi = None
        dirasakan = None
        
        
        for res in result:            
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text
            else:
                pass
            i += 1
                
        hasil = dict()
        hasil['tanggal'] = tanggal[0]
        hasil['waktu'] = tanggal[1]
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['koordinat'] = {'ls': koordinat[0], 'bt':koordinat[1]} 
        hasil['lokasi'] = lokasi
        hasil['dirasakan'] = dirasakan
        return hasil
    else:
        return None
        
        
def tampilkan_data(result):
    if result is None:
        print('Tidak bisa menemukan gempa terkini')
    
    print('Gempa Terakhir Berdasarkan BMKG')
    print('Tanggal :', result['tanggal'])
    print('Waktu :', result['waktu'])
    print('Magnitudo :', result['magnitudo'])
    print('Koordinat : LS', result['koordinat']['ls'], ' BT', result['koordinat']['bt'])
    print('Kedalaman :', result['kedalaman'])
    print('Lokasi :', result['lokasi'])
    print('Dirasakan :', result['dirasakan'])


if __name__ == '__main__':
    print('Earthquake Last Checker')
    res = ekstraksi_data()
    tampilkan_data(res)
