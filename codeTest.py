import sqlite3
from flask import Flask, request, render_template, flash, redirect
from models.search import Search

class Test():


    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def printName(self):
        sqlstr = "SELECT name FROM user"
        user = self.cursor.execute(sqlstr).fetchone()
        print(self.dbName)
        print(user)

    def printCounty(self):
        sqlstr = "SELECT distinct county FROM hospitals"
        county = self.cursor.execute(sqlstr).fetchall()
        cc = []
        for c in county:
            cc.append(c[0])
        return cc

    def printTownship(self):
        county = Test().printCounty()
        for c in county:
            sqlstr = "SELECT distinct township FROM hospitals WHERE county = '{}'".format(c)
            township = self.cursor.execute(sqlstr).fetchall()
            tt = [""]
            for t in township:
                tt.append(t[0])
            tt.append(c)
            print(c)
            print(tt)

    def printJS(self):
        areaStr = {
            '0': ['', ''],
            '1': ['', '安樂區', '信義區', '中正區', '暖暖區', '仁愛區', '七堵區', '中山區', '基隆市'],
            '2': ['', '大安區', '中正區', '中山區', '北投區', '內湖區', '士林區', '文山區', '松山區', '信義區', '大同區', '萬華區', '南港區', '臺北市'],
            '3': ['', '板橋區', '三峽區', '新莊區', '汐止區', '中和區', '新店區', '三重區', '永和區', '土城區', '瑞芳區', '金山區', '樹林區', '淡水區', '林口區',
                  '蘆洲區', '泰山區', '五股區', '鶯歌區', '深坑區', '貢寮區', '平溪區', '三芝區', '石碇區', '萬里區', '雙溪區', '八里區', '坪林區', '烏來區',
                  '石門區', '新北市'],
            '4': ['', '龜山區', '桃園區', '平鎮區', '龍潭區', '中壢區', '新屋區', '大園區', '楊梅區', '八德區', '大溪區', '觀音區', '蘆竹區', '復興區', '桃園市'],
            '5': ['', '竹北市', '湖口鄉', '竹東鎮', '新豐鄉', '新埔鎮', '關西鎮', '穹林鄉', '五峰鄉', '寶山鄉', '北埔鄉', '橫山鄉', '峨眉鄉', '尖石鄉', '新竹縣'],
            '6': ['', '東區', '北區', '香山區', '新竹市'],
            '7': ['', '頭份市', '苗栗市', '苑裡鎮', '大湖鄉', '竹南鎮', '通霄鎮', '公館鄉', '三灣鄉', '後龍鎮', '泰安鄉', '三義鄉', '卓蘭鎮', '銅鑼鄉', '頭屋鄉',
                  '南庄鄉', '西湖鄉', '造橋鄉', '獅潭鄉', '苗栗縣'],
            '8': ['', '北區', '西屯區', '南區', '梧棲區', '豐原區', '西區', '潭子區', '南屯區', '沙鹿區', '大里區', '大甲區', '太平區', '大雅區', '霧峰區',
                  '烏日區', '中區', '東勢區', '北屯區', '東區', '后里區', '清水區', '龍井區', '大肚區', '和平區', '新社區', '外埔區', '石岡區', '大安區', '神岡區',
                  '臺中市'],
            '9': ['', '彰化市', '埔心鄉', '鹿港鎮', '員林鎮', '田中鎮', '北斗鎮', '和美鎮', '二林鎮', '溪湖鎮', '伸港鄉', '大村鄉', '福興鄉', '花壇鄉', '永靖鄉',
                  '溪州鄉', '芬園鄉', '芳苑鄉', '埔鹽鄉', '秀水鄉', '田尾鄉', '大城鄉', '埤頭鄉', '竹塘鄉', '線西鄉', '二水鄉', '社頭鄉', '彰化縣'],
            '10': ['', '埔里鎮', '草屯鎮', '南投市', '竹山鎮', '鹿谷鄉', '水里鄉', '仁愛鄉', '集集鎮', '魚池鄉', '名間鄉', '國姓鄉', '中寮鄉', '信義鄉',
                   '南投縣'],
            '11': ['', '虎尾鎮', '斗六市', '北港鎮', '西螺鎮', '土庫鎮', '麥寮鄉', '斗南鎮', '褒忠鄉', '大埤鄉', '林內鄉', '崙背鄉', '口湖鄉', '古坑鄉', '刺桐鄉',
                   '臺西鄉', '二崙鄉', '東勢鄉', '元長鄉', '四湖鄉', '水林鄉', '雲林縣'],
            '12': ['', '東區', '西區', '嘉義市'],
            '13': ['', '大林鎮', '朴子市', '竹崎鄉', '民雄鄉', '溪口鄉', '新港鄉', '東石鄉', '六腳鄉', '鹿草鄉', '水上鄉', '義竹鄉', '太保市', '阿里山鄉',
                   '中埔鄉', '布袋鎮', '番路鄉', '梅山鄉', '嘉義縣'],
            '14': ['', '北區', '永康區', '南區', '麻豆區', '柳營區', '西區', '東區', '安南區', '仁德區', '中區', '新營區', '佳里區', '中西區', '關廟區',
                   '新化區', '善化區', '白河區', '安平區', '新市區', '後壁區', '七股區', '北門區', '鹽水區', '安定區', '下營區', '學甲區', '大內區', '官田區',
                   '東山區', '將軍區', '玉井區', '西港區', '歸仁區', '龍崎區', '左鎮區', '南化區', '山上區', '楠西區', '六甲區', '臺南市'],
            '15': ['', '三民區', '左營區', '鳥松區', '苓雅區', '前金區', '鼓山區', '小港區', '燕巢區', '楠梓區', '鳳山區', '林園區', '岡山區', '旗津區', '前鎮區',
                   '新興區', '旗山區', '橋頭區', '阿蓮區', '路竹區', '美濃區', '大寮區', '鹽埕區', '六龜區', '茄萣區', '大社區', '梓官區', '那瑪夏區', '仁武區',
                   '內門區', '甲仙區', '杉林區', '桃源區', '大樹區', '湖內區', '永安區', '茂林區', '彌陀區', '田寮區', '高雄市'],
            '16': ['', '東港鎮', '屏東市', '枋寮鄉', '恆春鎮', '內埔鄉', '高樹鄉', '潮州鎮', '春日鄉', '長治鄉', '林邊鄉', '三地鄉', '牡丹鄉', '獅子鄉', '鹽埔鄉',
                   '新埤鄉', '琉球鄉', '滿州鄉', '萬丹鄉', '九如鄉', '瑪家鄉', '車城鄉', '來義鄉', '新園鄉', '佳冬鄉', '萬巒鄉', '枋山鄉', '里港鄉', '泰武鄉',
                   '麟洛鄉', '崁頂鄉', '霧臺鄉', '南州鄉', '竹田鄉', '屏東縣'],
            '17': ['', '臺東市', '關山鎮', '成功鎮', '鹿野鄉', '太麻里', '蘭嶼鄉', '東河鄉', '長濱鄉', '池上鄉', '達仁鄉', '金峰鄉', '綠島鄉', '海端鄉', '卑南鄉',
                   '大武鄉', '延平鄉', '臺東縣'],
            '18': ['', '花蓮市', '新城鄉', '豐濱鄉', '玉里鎮', '鳳林鎮', '壽豐鄉', '吉安鄉', '瑞穗鄉', '光復鄉', '秀林鄉', '卓溪鄉', '富里鄉', '萬榮鄉',
                   '花蓮縣'],
            '19': ['', '宜蘭市', '羅東鎮', '礁溪鄉', '蘇澳鎮', '員山鄉', '壯圍鄉', '冬山鄉', '南澳鄉', '五結鄉', '三星鄉', '大同鄉', '頭城鎮', '宜蘭縣'],
            '20': ['', '馬公市', '湖西鎮', '七美鄉', '白沙鄉', '望安鄉', '西嶼鄉', '澎湖縣'],
            '21': ['', '金湖鎮', '金寧鎮', '金城鎮', '烈嶼鄉', '金沙鎮', '金門縣'],
            '22': ['', '南竿鄉', '北竿鄉', '東引鄉', '莒光鄉', '連江縣']
        }
        for i in range(23):
            dep = areaStr.get(str(i))
            dep.remove(dep[-1])
            dep[0] = "鄉鎮市區不拘"
            print("department[{}] = ".format(i) + str(dep) +';')

    def printAutocomplete(self):
        sqlstr = "SELECT abbreviation FROM hospitals"
        abbr = self.cursor.execute(sqlstr).fetchall()
        name = []
        for ab in abbr:
            name.append(ab[0])
        print(name)
        print(len(name))


# Test().printAutocomplete()

    def test(self, aa):
        sqlstr = "SELECT v_12, v_13, v_14 FROM merge_data WHERE hospital_id <5"
        sqlstr2 = "SELECT id, name FROM hospitals WHERE id<5"
        a = self.cursor.execute(sqlstr).fetchall()
        b = self.cursor.execute(sqlstr2).fetchall()
        c = [(4, '財團法人私立高雄醫學大學附設中和紀念醫院'), (1, '國泰醫療財團法人國泰綜合醫院'), (2, '長庚醫療財團法人林口長庚紀念醫院'), (3, '佛教慈濟醫療財團法人花蓮慈濟醫院')]
        print(a)
        print(b)
        print(c)
        # print(sorted(a, reverse=True))  ## 遞減
        # print(sorted(a))  ## 遞增
        # print(sorted(a, key=lambda l : l[1]))  ## 按index1排序
        z =zip(a, b, c)
        print(sorted(z, key = lambda l: l[2][0], reverse=True))  ##按照zip中「0位置的陣列」中的「2位置的資料」遞增排序-->a[2]的資料

    def default(self, indexes, sql_where, reserved):
        substr = ''
        for index in indexes:
            substr += 'fd.d_{},'.format(index)
        substr = substr[:-1]  #刪除最後一個逗號#

        sqlstr = ("SELECT MAX({}) FROM merge_data m LEFT JOIN hospitals h ON m.hospital_id = h.id LEFT JOIN final_reviews fr ON h.id = fr.hospital_id LEFT JOIN final_data fd ON h.id = fd.hospital_id ".format(substr)) + sql_where
        all_deno = self.cursor.execute(sqlstr).fetchall()
        print(sqlstr)
        print(all_deno)

        # hosp_id = []
        # boolean = []
        # for deno in all_deno:

Test().default(['44', '13', '15'],"WHERE (h.area LIKE '%%')AND (h.type = '醫學中心') AND ((m.v_44 != -1) OR (m.v_13 != -1) OR (m.v_15 != -1))",'')
