**KURULUM**

- Gereksinimler:
    python 3.8+, cv2, numpy, pil, flask, sqlite3, os
  
1.  python 3.8 veya daha yeni bir sürümünü kurun.
2.  Gereksinimlerde belirtilen gerekli kütüphaneleri yükleyin.
3.  Veri tabanını oluşturmak için vt.py çalıştırın.
4.  Kurulum tamamlandıktan sonra app.py çalıştırın.
5.  Tarayıcınızdan http://localhost:5000/ adresine girin. Bu ekranı açılış ekranı olarak tabir edeceğiz.

**KULANIM**

1.  Veri tabanı yeni oluşturulduğundan sadece yönetici hesabı mevcuttur. 
    Kullanıcı adı: admin ve şifre: admin olarak giriş yapabilirsiniz.
2.  Kullanıcı kaydı yapmadan önce admin olarak giriş yapıp birim kaydı yapmalısınız.
3.  Henüz giriş yapmadıysanız açılış ekranın sağ üst köşesinde bulunan "Giriş Yap" seçeneğini kullanarak giriş 
    yapabilir veya "Kayıt Ol" seçeneğini kullanarak kayıt olabilirsiniz.
4.  Açılış ekranından erişebildiğiniz "Kayıt Ol" seçeneği çalışanlar içindir. Yönetici kaydı için admin hesabını
    kullanarak yeni yönetici ekleyebilir ve güncellemeler yapabilirsiniz.
5.  Kayıt ve Giriş aşamalarını geçtikten sonra "Menü" ekranına yönlendirileceksiniz.
6.  Yönetici hesabıyla giriş yaptığınızda yönetici, çalışan veya ziyaretçi ekleyebilir, güncelleme ve silme 
    yapabilirsiniz. Aynı zamanda tüm kameralara erişebilir, yeni kameralar ekleyebilir ve çalışanların erişebileceği
    kameraları yönetebilirsiniz.
7.  Çalışan hesabı ile giriş yaptığınızda ziyaretçi ekleyebilir ve erişiminize izin verilen kameraları izleyebilirsiniz.