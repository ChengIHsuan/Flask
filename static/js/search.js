
// 指標說明滾動
$(document).ready(function () {
    $(".explain").click(function () {
        $('html, body').animate({
            scrollTop: $("#searchEx").offset().top
        });
    });
});

// 搜尋頁籤
$(function () {
    $("#tabs-nav a").click(function () {
        $("#tabs-nav a").removeClass("tabs-menu-active");
        $(this).addClass("tabs-menu-active");
        $(".tabs-panel").hide();
        var tab_id = $(this).attr("href");
        $(tab_id).fadeIn();
        return false;
    });
});

//縣市連動
department = new Array();
department[0] = ["鄉鎮市區不拘"];
department[1] = ["鄉鎮市區不拘", "安樂區", "信義區", "中正區", "暖暖區", "仁愛區", "七堵區", "中山區"];
department[2] = ["鄉鎮市區不拘", "大安區", "中正區", "中山區", "北投區", "內湖區", "士林區", "文山區", "松山區", "信義區", "大同區", "萬華區", "南港區"];
department[3] = ["鄉鎮市區不拘", "板橋區", "三峽區", "新莊區", "汐止區", "中和區", "新店區", "三重區", "永和區", "土城區", "瑞芳區", "金山區", "樹林區", "淡水區", "林口區", "蘆洲區", "泰山區", "五股區", "鶯歌區", "深坑區", "貢寮區", "平溪區", "三芝區", "石碇區", "萬里區", "雙溪區", "八里區", "坪林區", "烏來區", "石門區"];
department[4] = ["鄉鎮市區不拘", "龜山區", "桃園區", "平鎮區", "龍潭區", "中壢區", "新屋區", "大園區", "楊梅區", "八德區", "大溪區", "觀音區", "蘆竹區", "復興區"];
department[5] = ["鄉鎮市區不拘", "竹北市", "湖口鄉", "竹東鎮", "新豐鄉", "新埔鎮", "關西鎮", "穹林鄉", "五峰鄉", "寶山鄉", "北埔鄉", "橫山鄉", "峨眉鄉", "尖石鄉"];
department[6] = ["鄉鎮市區不拘", "東區", "北區", "香山區", "東區林"];
department[7] = ["鄉鎮市區不拘", "頭份市", "苗栗市", "苑裡鎮", "大湖鄉", "竹南鎮", "通霄鎮", "公館鄉", "三灣鄉", "後龍鎮", "泰安鄉", "三義鄉", "卓蘭鎮", "銅鑼鄉", "頭屋鄉", "南庄鄉", "西湖鄉", "造橋鄉", "獅潭鄉"];
department[8] = ["鄉鎮市區不拘", "北區", "西屯區", "南區", "梧棲區", "豐原區", "西區", "潭子區", "南屯區", "沙鹿區", "大里區", "大甲區", "太平區", "大雅區", "霧峰區", "烏日區", "中區", "東勢區", "北屯區", "東區", "后里區", "清水區", "龍井區", "大肚區", "和平區", "新社區", "外埔區", "石岡區", "大安區", "神岡區", "南區民", "南區新", "西區蔡", "北區鴻"];
department[9] = ["鄉鎮市區不拘", "彰化市", "埔心鄉", "鹿港鎮", "員林鎮", "田中鎮", "北斗鎮", "和美鎮", "二林鎮", "溪湖鎮", "伸港鄉", "大村鄉", "福興鄉", "花壇鄉", "永靖鄉", "溪州鄉", "芬園鄉", "芳苑鄉", "埔鹽鄉", "秀水鄉", "田尾鄉", "大城鄉", "埤頭鄉", "竹塘鄉", "線西鄉", "二水鄉", "社頭鄉"];
department[10] = ["鄉鎮市區不拘", "埔里鎮", "草屯鎮", "南投市", "竹山鎮", "鹿谷鄉", "水里鄉", "仁愛鄉", "集集鎮", "魚池鄉", "名間鄉", "國姓鄉", "中寮鄉", "信義鄉"];
department[11] = ["鄉鎮市區不拘", "虎尾鎮", "斗六市", "北港鎮", "西螺鎮", "土庫鎮", "麥寮鄉", "斗南鎮", "褒忠鄉", "大埤鄉", "林內鄉", "崙背鄉", "口湖鄉", "古坑鄉", "刺桐鄉", "臺西鄉", "二崙鄉", "東勢鄉", "元長鄉", "四湖鄉", "水林鄉"];
department[12] = ["鄉鎮市區不拘", "東區", "西區"];
department[13] = ["鄉鎮市區不拘", "大林鎮", "朴子市", "竹崎鄉", "民雄鄉", "溪口鄉", "新港鄉", "東石鄉", "六腳鄉", "鹿草鄉", "水上鄉", "義竹鄉", "太保市", "阿里山", "中埔鄉", "布袋鎮", "番路鄉", "梅山鄉"];
department[14] = ["鄉鎮市區不拘", "北區", "永康區", "南區", "麻豆區", "營區", "西區", "東區", "安南區", "仁德區", "中區", "新營區", "佳里區", "中西區", "關廟區", "新化區", "善化區", "白河區", "安平區", "新市區", "後壁區", "七股區", "北門區", "鹽水區", "安定區", "下營區", "學甲區", "大內區", "官田區", "東山區", "將軍區", "玉井區", "西港區", "歸仁區", "龍崎區", "左鎮區", "南化區", "山上區", "楠西區", "六甲區", "北區弘", "北區惠", "南區民"];
department[15] = ["鄉鎮市區不拘", "三民區", "左營區", "鳥松區", "苓雅區", "前金區", "鼓山區", "小港區", "燕巢區", "楠梓區", "鳳山區", "林園區", "岡山區", "旗津區", "前鎮區", "新興區", "旗山區", "橋頭區", "阿蓮區", "路竹區", "美濃區", "大寮區", "鹽埕區", "六龜區", "茄萣區", "大社區", "梓官區", "那瑪夏區", "仁武區", "內門區", "甲仙區", "杉林區", "桃源區", "大樹區", "湖內區", "永安區", "茂林區", "彌陀區", "田寮區"];
department[16] = ["鄉鎮市區不拘", "東港鎮", "屏東市", "枋寮鄉", "恆春鎮", "內埔鄉", "高樹鄉", "潮州鎮", "春日鄉", "長治鄉", "林邊鄉", "三地鄉", "牡丹鄉", "獅子鄉", "鹽埔鄉", "新埤鄉", "琉球鄉", "滿州鄉", "萬丹鄉", "九如鄉", "瑪家鄉", "車城鄉", "來義鄉", "新園鄉", "佳冬鄉", "萬巒鄉", "枋山鄉", "里港鄉", "泰武鄉", "麟洛鄉", "崁頂鄉", "霧臺鄉", "南州鄉", "竹田鄉"];
department[17] = ["鄉鎮市區不拘", "臺東市", "關山鎮", "成功鎮", "鹿野鄉", "太麻里", "蘭嶼鄉", "東河鄉", "長濱鄉", "池上鄉", "達仁鄉", "金峰鄉", "綠島鄉", "海端鄉", "卑南鄉", "大武鄉", "延平鄉"];
department[18] = ["鄉鎮市區不拘", "花蓮市", "新城鄉", "豐濱鄉", "玉里鎮", "鳳林鎮", "壽豐鄉", "吉安鄉", "瑞穗鄉", "光復鄉", "秀林鄉", "卓溪鄉", "富里鄉", "萬榮鄉"];
department[19] = ["鄉鎮市區不拘", "宜蘭市", "羅東鎮", "礁溪鄉", "蘇澳鎮", "員山鄉", "壯圍鄉", "冬山鄉", "南澳鄉", "五結鄉", "三星鄉", "大同鄉", "頭城鎮"];
department[20] = ["鄉鎮市區不拘", "馬公市", "湖西鎮", "七美鄉", "白沙鄉", "望安鄉", "西嶼鄉"];
department[21] = ["鄉鎮市區不拘", "金湖鎮", "金寧鎮", "金城鎮", "烈嶼鄉", "金沙鎮"];
department[22] = ["鄉鎮市區不拘", "南竿鄉", "北竿鄉", "東引鄉", "莒光鄉"];
//特疾地區
function renew(index) {
    for (var i = 0; i < department[index].length; i++)
        document.myForm.township.options[i] = new Option(department[index][i], department[index][i]);	// 設定新選項
    document.myForm.township.length = department[index].length;	// 刪除多餘的選項
}
// 科別地區
function renew2(index) {
    for (var i = 0; i < department[index].length; i++)
        document.myForm.township2.options[i] = new Option(department[index][i], department[index][i]);	// 設定新選項
    document.myForm.township2.length = department[index].length;	// 刪除多餘的選項
}
// 醫療機構地區
function renew3(index) {
    for (var i = 0; i < department[index].length; i++)
        document.myForm.township3.options[i] = new Option(department[index][i], department[index][i]);	// 設定新選項
    document.myForm.township2.length = department[index].length;	// 刪除多餘的選項
}

//名稱自動完成
$(function () {
    var name = ['國泰醫院總院', '林口長庚', '花蓮慈濟', '高雄中和', '成大醫院總院', '彰化基督教醫院', '中國醫總院', '台中榮總總院', '台大醫院總院', '亞東醫院', '高雄榮總總院', '高雄長庚', '中山醫總院', '馬偕醫院', '臺北榮總總院'];
     $(".name").autocomplete({
        source: name
    }
    );
});

//分頁
$(function () {
    var $table = $('table');
    var $tableB = $('h2');
    var currentPage = 0;//當前頁默認值為0
    var pageSize = 15 * 4;//每一頁顯示的數目

    $table.bind('paging', function () {
        $table.find('tbody tr').hide().slice(currentPage * pageSize, (currentPage + 1) * pageSize).show();
    });
    var sumRows = $table.find('tbody tr').length;
    var sumPages = Math.ceil(sumRows / pageSize);//總頁數
    var large = sumPages * 36;
    var $pager = $('<div class="page" style="width:' + large + 'px" ></div>');  //新建div，放入a標籤,顯示底部分頁碼
    for (var pageIndex = 0; pageIndex < sumPages; pageIndex++) {
        $('<a href="#thead" id="pageStyle" onclick="changCss(this)"><span>' + (pageIndex + 1) + '</span></a>').bind("click", { "newPage": pageIndex }, function (event) {
            currentPage = event.data["newPage"];
            $table.trigger("paging");

            //觸發分頁函數
        }).appendTo($pager);
        $pager.append(" ");

    }
    $pager.insertAfter($tableB);
    $table.trigger("paging");
    //默認第一頁的a標籤效果
    var $pagess = $('#pageStyle');
    $pagess[0].style.backgroundColor = "rgb(101,129,152)";
    $pagess[0].style.color = "#ffffff";
});

//a鏈接點擊變色，再點其他回覆原色
function changCss(obj) {
    var arr = document.getElementsByTagName("a");
    for (var i = 0; i < arr.length; i++) {
        if (obj == arr[i]) {       //當前頁樣式
            obj.style.backgroundColor = "rgb(101,129,152)";
            obj.style.color = "#ffffff";
        }
        else {
            arr[i].style.color = "";
            arr[i].style.backgroundColor = "";
        }
    }

}
////////////////////////////////////////////////////////////////////
jQuery(document).ready(function () {
    var offset = 220;
    var duration = 500;
    jQuery(window).scroll(function () {
        if (jQuery(this).scrollTop() > offset) {
            jQuery('.back-to-top').fadeIn(duration);
        } else {
            jQuery('.back-to-top').fadeOut(duration);
        }
    });

    jQuery('.back-to-top').click(function (event) {
        event.preventDefault();
        jQuery('html, body').animate({ scrollTop: 0 }, duration);
        return false;
    })
});
// 特疾與指標必選
var flag = 0;
var ckIndex = document.getElementsByName("ckIndex");
var btnSearch = document.getElementById("btnSearch");
var items = document.getElementsByName("ckIndex");
function indexSelect() {
    var no = document.getElementById("no");
    var as = document.getElementById("asthma");
    var ami = document.getElementById("ami");
    var di = document.getElementById("diabetes");
    var kn = document.getElementById("knee");
    var br = document.getElementById("brain");
    var si = document.getElementById("sinusitis");
    var ut = document.getElementById("uterus");
    var pu = document.getElementById("pu");
    var bl = document.getElementById("blood");
    var kw = document.getElementById("kw");
    var dis = document.getElementById("disease").value;
    switch (dis) {
        case "no":
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
            no.style.display = "block";
            as.style.display = "none";
            ami.style.display = "none";
            di.style.display = "none";
            kn.style.display = "none";
            br.style.display = "none";
            si.style.display = "none";
            ut.style.display = "none";
            pu.style.display = "none";
            bl.style.display = "none";
            kw.style.display = "none";
            for (i = 0; i < ckIndex.length; i++) {
                if (ckIndex[i].checked) {
                    flag--;
                }
                ckIndex[i].checked = false;
                items[i].disabled = false;
            }
            break;

        case "1":
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
            no.style.display = "none";
            as.style.display = "block";
            ami.style.display = "none";
            di.style.display = "none";
            kn.style.display = "none";
            br.style.display = "none";
            si.style.display = "none";
            ut.style.display = "none";
            pu.style.display = "none";
            bl.style.display = "none";
            kw.style.display = "none";
            for (i = 0; i < ckIndex.length; i++) {
                if (ckIndex[i].checked) {
                    flag--;
                }
                ckIndex[i].checked = false;
                items[i].disabled = false;
            }
            break;
        case "2":
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
            no.style.display = "none";
            as.style.display = "none";
            ami.style.display = "block";
            di.style.display = "none";
            kn.style.display = "none";
            br.style.display = "none";
            si.style.display = "none";
            ut.style.display = "none";
            pu.style.display = "none";
            bl.style.display = "none";
            kw.style.display = "none";
            for (i = 0; i < ckIndex.length; i++) {
                if (ckIndex[i].checked) {
                    flag--;
                }
                ckIndex[i].checked = false;
                items[i].disabled = false;
            }
            break;
        case "3":
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
            no.style.display = "none";
            as.style.display = "none";
            ami.style.display = "none";
            di.style.display = "block";
            kn.style.display = "none";
            br.style.display = "none";
            si.style.display = "none";
            ut.style.display = "none";
            pu.style.display = "none";
            bl.style.display = "none";
            kw.style.display = "none";
            for (i = 0; i < ckIndex.length; i++) {
                if (ckIndex[i].checked) {
                    flag--;
                }
                ckIndex[i].checked = false;
                items[i].disabled = false;
            }
            break;
        case "4":
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
            no.style.display = "none";
            as.style.display = "none";
            ami.style.display = "none";
            di.style.display = "none";
            kn.style.display = "block";
            br.style.display = "none";
            si.style.display = "none";
            ut.style.display = "none";
            pu.style.display = "none";
            bl.style.display = "none";
            kw.style.display = "none";
            for (i = 0; i < ckIndex.length; i++) {
                if (ckIndex[i].checked) {
                    flag--;
                }
                ckIndex[i].checked = false;
                items[i].disabled = false;
            }
            break;
        case "5":
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
            no.style.display = "none";
            as.style.display = "none";
            ami.style.display = "none";
            di.style.display = "none";
            kn.style.display = "none";
            br.style.display = "block";
            si.style.display = "none";
            ut.style.display = "none";
            pu.style.display = "none";
            bl.style.display = "none";
            kw.style.display = "none";
            for (i = 0; i < ckIndex.length; i++) {
                if (ckIndex[i].checked) {
                    flag--;
                }
                ckIndex[i].checked = false;
                items[i].disabled = false;
            }
            break;
        case "6":
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
            no.style.display = "none";
            as.style.display = "none";
            ami.style.display = "none";
            di.style.display = "none";
            kn.style.display = "none";
            br.style.display = "none";
            si.style.display = "block";
            ut.style.display = "none";
            pu.style.display = "none";
            bl.style.display = "none";
            kw.style.display = "none";
            for (i = 0; i < ckIndex.length; i++) {
                if (ckIndex[i].checked) {
                    flag--;
                }
                ckIndex[i].checked = false;
                items[i].disabled = false;
            }
            break;
        case "7":
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
            no.style.display = "none";
            as.style.display = "none";
            ami.style.display = "none";
            di.style.display = "none";
            kn.style.display = "none";
            br.style.display = "none";
            si.style.display = "none";
            ut.style.display = "block";
            pu.style.display = "none";
            bl.style.display = "none";
            kw.style.display = "none";
            for (i = 0; i < ckIndex.length; i++) {
                if (ckIndex[i].checked) {
                    flag--;
                }
                ckIndex[i].checked = false;
                items[i].disabled = false;
            }
            break;
        case "8":
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
            no.style.display = "none";
            as.style.display = "none";
            ami.style.display = "none";
            di.style.display = "none";
            kn.style.display = "none";
            br.style.display = "none";
            si.style.display = "none";
            ut.style.display = "none";
            pu.style.display = "block";
            bl.style.display = "none";
            kw.style.display = "none";
            for (i = 0; i < ckIndex.length; i++) {
                if (ckIndex[i].checked) {
                    flag--;
                }
                ckIndex[i].checked = false;
                items[i].disabled = false;
            }
            break;
        case "9":
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
            no.style.display = "none";
            as.style.display = "none";
            ami.style.display = "none";
            di.style.display = "none";
            kn.style.display = "none";
            br.style.display = "none";
            si.style.display = "none";
            ut.style.display = "none";
            pu.style.display = "none";
            bl.style.display = "block";
            kw.style.display = "none";
            for (i = 0; i < ckIndex.length; i++) {
                if (ckIndex[i].checked) {
                    flag--;
                }
                ckIndex[i].checked = false;
                items[i].disabled = false;
            }
            break;
        case "10":
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
            no.style.display = "none";
            as.style.display = "none";
            ami.style.display = "none";
            di.style.display = "none";
            kn.style.display = "none";
            br.style.display = "none";
            si.style.display = "none";
            ut.style.display = "none";
            pu.style.display = "none";
            bl.style.display = "none";
            kw.style.display = "block";
            for (i = 0; i < ckIndex.length; i++) {
                if (ckIndex[i].checked) {
                    flag--;
                }
                ckIndex[i].checked = false;
                items[i].disabled = false;
            }
            break;
        default:
    }
}

// 判斷5個以上不能選,指標必選
var maxChoices = 5;

function onCheckBox(checkbox) {

    if (checkbox.checked) {
        flag++;
    }
    else {
        flag--;
    }

    if (flag < maxChoices) {
        if (flag == 0) {
            $('#btnSearch').attr('disabled', true);
            $('#btnSearchOb').attr('disabled', true);
        }
        else {
            $('#btnSearch').attr('disabled', false);
            $('#btnSearchOb').attr('disabled', false);
        }
        for (var i = 0; i < items.length; i++) {
            if (!items[i].checked) {
                items[i].disabled = false;
            }
        }
    }
    else {
        for (var i = 0; i < items.length; i++) {
            if (!items[i].checked) {
                items[i].disabled = true;
            }
        }
    }
}

//必選科別指標，必選主觀指標
var sub = 0;
var itemsSub = document.getElementsByName("subjective");
function onCheckBoxSub(checkbox) {
    if (checkbox.checked) {
        sub++;
    }
    else {
        sub--;
    }
    if (sub <= 0) {
        $('#btnSearchB').attr('disabled', true);
        $('#btnSearchSub').attr('disabled', true);
    } else {
        $('#btnSearchB').attr('disabled', false);
        $('#btnSearchSub').attr('disabled', false);
    }
}

//必選客觀指標
var ob = 0;
var itemsOb = document.getElementsByName("ckIndex");
function onCheckBoxOb(checkbox) {
    if (checkbox.checked) {
        ob++;
    }
    else {
        ob--;
    }
    if (sub <= 0) {

        $('#btnSearchOb').attr('disabled', true);
    } else {

        $('#btnSearchOb').attr('disabled', false);
    }
}



