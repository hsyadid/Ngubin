# toko_ngubin

## Link PWS

Web dapat diakses melalui <http://hubban-syadid-ngubin.pbp.cs.ui.ac.id/>

## Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?

_Proses data delivery menjadi aspek penting dalam pengembangan sebuah platform
Dikarenakan, seringkali platform yang kita buat ingin berkomunikasi dengan sebuah sistem lain melalui sebuah API dan semacamnya, data delivery memastikan data dikirim dan juga diterima dalam bentuk yang dapat di akses dan diproses oleh berbagai sistem, contoh nya adalah menggunakan XML dan juga JSON._

## Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?

_Dikarenakan format JSOn lebih flexibel dan juga mudah diolah dibandingkan bentuk XML. JSON memiliki struktur yang sederhana dan mudah untuk dibaca oleh manusia.Struktur yang diimplementasikan oleh JSON adalah key-value pair yang mana ini berbeda dengan XML yang memiliki tag penutup dan pembuka. Dari segi parsing pun JSON lebih cepat untuk di parse daripada XML ini berakibat dari strukturnya yang sederhana. Ukuran file json pun biasanya juga lebih kecil jika dibandingkan dengan XML_

## Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?

_Dikarenakan method ini berfungsi untuk mengecek apakah input yang telah dimasukkan oleh user telah sesuai atau belum dengan kriteria yang telah di kita definisikan dalam form sebelumnya, seperti panjang string maupun angka dalam rentang tertentu.dan jika kiat tidak mengimplementasikan method ini kita tidak bisa memberikan umpan balik kesalahan yang jelas kepada pengguna._

## Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?

_Pada saat data delivery csrf_token di peruntukan untuk aspek keamanan contoh yang dapat membahayakan aplikasi contoh nya adalah serangan CSRF (Cross-Site Request Forgery). Pada serangan ini penyerang bisa saja membuat request yang tampak nya valid dari sumber yang sebenarnya tidak sah. Dan cara kerja dari pun cukup mudah dimengerti dengan menambahkan token CSRF ke dalam formulir, nantinya django bisa memverifikasi apakah kode ini berasal dari sesi pengguna yang sama atau tidak._

_Jika kita tidak menambahkan csrf_token pada form yang kita buat, tentu aplikasi kita akan rentan terhadap serangan CSRF, yang mana ini berbahaya dikarenakan penyerang dapat mengubah pengaturan akun pengguna atau pun melakukan transaksi finansial atau mengirimkan data yang tidak diinginkan tanpa sepengetahuan dari pengguna. Kesimpulan penggunaan csrf_token itu penting untuk menghindari eksploitasi data pribadi._

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial) ?

## Contoh http response mengunakan metode get

![xml](media/xml_data.jpg)
![json](media/json_data.jpg)
![xml_id](media/xml_id.jpg)
![json_id](media/json_id.jpg)
