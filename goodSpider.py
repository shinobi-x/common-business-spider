# -*- coding: utf-8 -*-

import config

import bs4
import requests
import re, os, time, sys
import logging, logging.handlers
import argparse

import JdGoodsPage
import JdLogin
import UploadData
import JdItemsPage
import urlparse


reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
# 改变目录
os.chdir(sys.path[0])


class GoodSpider(object):
	def __init__(self):
		
		self.sess = object
		self.cookies = {}
		self.finish = ''
		self.sleep_time = config.SLEEP_TIMEPAGE_DONE
		self.get_items_host = config.BASE_GET_ITEMS_HOST

		# logger = logging.getLogger('goodSpider')
		# logger.setLevel(logging.INFO)
		# rh=logging.handlers.TimedRotatingFileHandler('log/goodspider.log', 'D')
		# fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		# rh.setFormatter(fm)
		# logger.addHandler(rh)
		# self.infolog=logger.info
		# self.errorlog=logger.error

		self.jdgoodspage = JdGoodsPage.JdGoodsPage()
		self.jdlogin = JdLogin.JdLogin()
		self.uploaddata = UploadData.UploadData()
		self.uploaddata.set_csv_file_path(config.BASE_SKUID_CSV_FILE)
		self.uploaddata.set_csv_uniq_file_path(config.BASE_SKUID_CSV_UNIQ_FILE)
		self.uploaddata.set_upload_host(config.BASE_UPLOAD_ITMES_HOST)
		self.JdItemsPageSpider = JdItemsPage.JdItemsPage()



	def jd_login(self):
		if self.jdlogin.check_login():
			self.sess = self.jdlogin.get_sess()
			self.cookies = self.jdlogin.get_cookies()
			return True
		else:
			return False



	def goods_page(self, url):
		self.jdgoodspage.set_sess(self.sess)
		self.jdgoodspage.set_cookies(self.cookies)
		items = []
		items = self.jdgoodspage.goods_page(url)
		# print items
		# self.infolog('商品数: %d', len(items))
		if len(items) < 1:
			self.finish = True
			return
		try:
			rs = urlparse.urlparse(url)
			q = urlparse.parse_qs(rs.query)
			# if 'keyword' in q:
			# 	skuid = q['keyword'][0]
			# 	tmp = self.JdItemsPageSpider.items_page_pc('https://item.jd.com/' + str(skuid) + '.html')
			# 	if tmp != False and tmp != None and len(tmp) > 0:
			# 		items[0]['category1'] = tmp['category1']
			# 		items[0]['adownerType'] = tmp['adownerType']
			self.uploaddata.save_items_to_file(items)
			time.sleep( self.sleep_time )
		except Exception, e:
			# self.errorlog('Exp2 {0} : {1}'.format(FuncName(), e))
			pass



	def goods_category(self, category):
		url = 'https://media.jd.com/gotoadv/goods?pageIndex=&pageSize=10&property=&sort=&adownerType=&pcRate=&wlRate=&category=&category1=0&condition=0&fromPrice=&toPrice=&goodsView=list&keyword=' + str(category['keyword'])
		# print url
		# self.infolog(url)
		self.goods_page(url)



	def category_list(self):
		goodsItems = self.get_items()
		print u'待更新商品总数: ' + str(len(goodsItems))
		# goodsItems = ['11475910464','11677993862','10701481924','1116621738','1728981668','10125765170','10061146016','12493137691','12658017760','11027662321','11189638801','1658129801','1343185831','10532641078','10557914287','10196799448','10261030958','10490836618','10694402073','10075392402','12049689051','11443803684','11465916075','11127253910','11264125287','12294846920','12532882763','12358424175','10150710017','1379559155','10108787754','1343544024','1442108634','1576042117','10505717105','10764249151','11193859500','11440869155','10479922326','12634174849','1688958677','10647049049','11026756276','11972350552','10093297911','1637691738','10949551579','10833351582','10136286715','11305243359','10706273127','10828773991','10478677488','1746206220','11770024873','10592527518','1676156851','10658784927','1741771621','1041443116','11061735559','12067234229','1790094107','1762719485','11154433537','11681242478','10956275320','11463378877','11893178464','11154433537','11475910464','1636025220','1139451949','10341458030','11106443704','1475184605','10401509970','1546160330','10984949252','1740454266','12049689051','11253231250','11594104849','12358424174','12358424175','11264125287','12294846920','11574755478','10150745446','10150752716','10733169528','1539043187','10158123471','10156933469','1535253522','10112097210','1661810273','10146650281','10541465970','10091741590','1116698526','10299582853','10108787754','1343544024','1442108634','1576042117','11193859500','11440869155','11866255941','10263815831','1688958677','10647049049','11026756276','11972350552','10093297911','1637691738','10949551579','10833351582','10136286715','11305243359','10706273127','1347787044','10143244099','1746206220','11093974627','10535929293','1592526573','1694819161','11689573659','1041443116','11076691779','11523705535','1100610559','11318224684','10901549632','10919035342','12264603673','12081905651','11203102879','10682364496','4369996','3836885','4903502','4903500','3662618','1915369','3407234','3407258','4903598','3806453','12036422780','10710907338','10183520951','10663169084','1753120596','1486716028','10555347964','10809319641','10771485161','10554515353','3773218','3175636','3522099','3522081','4112901','3758992','4829966','2891518','2785535','2228287','4829968','664486','2511646','974864','2728382','2728378','3518501','1843432','3505232','2497008','1111418','688377','4374114','2441623','2234133','3171319','3154645','1210441','383881','3730238','3907129','4556376','2229736','3447571','2331644','1780924','4264866','3694340','4813030','3753594','2297879','3809261','2297186','4315552','4315566','1175434','3349874','2511669','3053891','1300999','3693804','2752973','3939873','3215647','2297200','3903330','3949937','2722595','2782534','3423762','3423766','3423768','4596108','4596106','3949931','1352438','5032214','5032216','4667744','5170824','4015468','2872478','2808881','4014403','5010856','4725704','4492062','3612060','4578684','3945945','5192730','1862177','4702874','4203829','1636340','1948548','4328018','975997','987394','5119852','5119858','4133630','1183796','2593925','10948604728','11564360510','1133915435','11742680383','10099552284','11254744274','10082675390','11889676211','10392904330','10884044790','11595823185','11596310384','11021342403','1587003359','10549918896','10448853795','10448412174','10987445730','1787300623','1521935901','10494209226','10321402830','10196547858','10624668850','11453829558','11368799484','11359891406','11338501440','1573720312','10464824561','11300272275','1256928433','11326424367','11471133008','1791148365','1689097406','1257352928','11039266077','10432709615','10107598208','11991274807','10321490808','10883916170','1686787544','10135984195','1736585231','1757584111','10732910564','10812284500','10700113418','12264005482','1504993946','10901968936','10950422459','10617046231','10084669793','10901968936','10617046231','10379457077','10372971761','10321467310','1625794481','10956533452','10450589694','1644891002','10031188689','1240151188','1181282564','1724558444','11253430670','1461567331','11253430661','1790040003','1790040004','1470446935','1471031013','1470820247','10719482345','1728908320','1803358745','1792235181','10447600849','10447600850','10075960608','12538227167','10075974775','10532805321','11972711323','11249708957','11331326256','10168663464','10620484271','10135833518','10642136046','11716184000','10899701143','1512671626','1785188765','11149798490','12036020636','12668936769','12536389640','11945179584','11903042647','12203405495','12203405500','11817946423','1643103468','10057438065','1746124826','10403572811','10554662994','11490883966','10392987945','10401987502','10401711806','11455507287','1468239179','10581987564','11974683686','10649522780','10420402031','10557774948','11932053518','10044468799','1749221296','1803529402','169498116','1712777709','1696935458','1750521145','1750509933','10768339926','10796362271','1749278577','1698551519','10354487801','1700500775','10604097385','10223611344','10579091593','11258700107','10948257252','11455946959','10339209678','10395156512','10382674683','10510986780','1787190148','1698576403','10093082279','1511267660','10420389693','12333636117','10093082277','10104161817','11632274368','11666270062','11666703792','11620808298','1640840474','1643658273','12193605910','10763883737','12204269047','12280966981','10943185913','1566777822','1470365493','1791037456','10996557191','10060803279','11972182658','11972182652','12036376445','11114924076','10093331568','10093370437','10093499396','1481570401','1548796540','1474196331','11941613961','1639692387','1626310121','1638220515','1696369272','1512234969','10285763043','1548796541','1548940024','12673114305','10342231306','1523775386','1568931973','10622476728','11944160897','12695814371','1522261941','2915809','3152946','4286306','3027128','1015341','3969267','4082696','2877919','10354023413','10450936475','10873597314','11968154708','12553851948','11572858830','11572858829','11384308350','11609162607','11700895931','11384060008','11346549348','11346549347','12399663813','12399663816','10941037480','11258458942','11441329984','11728495617','10925628511','10925628504','11054930262','11930118823','11930189849','11879051478','12099475219','10561956169','11632253460','1642104439','11654952875','10504623160','10279469627','11782991039','10527257564','12314953938','10399361065','10876827756','10678692069','12047161310','11607046289','10117969678','10165416932','12395340905','11775111','12094060','12697443021','11861488943','11797536837','12576396793','10227487508','12713497203','11544607836','11542205766','11544315264','12713497203','11544607836','11542205766','11544315264','11285336324','1439674990','11641021324','10989239993','10122577281','12376127064','12656145049','11564755659','10148997028','1817682055','10380996265','11986332506','11609198295','10088480789','10243435891','10791441405','12441018692','1794369980','11688904452','11201824191','10450767827','12712669526','11519958024','11261691964','12110422052','11655856836','10736451131','11562414762','12095365775','10741833973','11044898765','10135098861','10546025934','10274243639','10510631631','12401228792','10116894187','11728938612','12674453924','11253129782','1811239045','10601256177','10907668280','11011495736','11282181831','10849304204','10876652511','10809259212','10447632966','10017425772','12154069944','12259316763','1523437783','12653456675','11742237847','11050693807','11016926930','10930591780','11946042263','11687602306','11619300895','10421609204','10505433589','11959217452','11944638544','12051628393','10245201764','1815229406','12575721988','12275093839','10711765545','1626313505','10827079086','11184038928','11629600557','12187391660','10257916044','12083132530','12048255647','12171901874','11666819086','10276852198','1623285424','12401659820','12155134897','10034517855','1619108436','11489179753','11184100481','11534322492','12315415346','10519095651','10257955996','12416828797','11955409888','10164886643','11536816830','10276852196','10619526062','12028077','12028079','11240828248','11675730934','12373052143','10355697441','12003004833','10866845742','12067774124','10399336952','11392421268','10745450149','12514324501','11985565561','12421604515','11732408149','10276852197','1423618303','12086514','11999664','11903442','12001214','12000594','11952855','10281763','10037924','10217787','10038006','11933832','12024294','12022583','12023639','12062807','11300777','11933834','10786663458','1154480861','12595508721','11690686014','12110390405','12154961434','12174482373','10992610680','10991249819','12594812132','12674232637','12270977097','10242971876','12190330876','10375044529','11234026644','11927010987','10673567878','11973041834','11801904485','10513732817','10695809246','11985503152','11605915583','12315571218','11944213182','1252812682','11781048823','11780946183','11780250891','11780256658','11781031224','12276346451','1247890286','11454962910','10940186539','11780929647','11780925476','11769104826','11555555045','1247464483','12171580435','11441208712','11441264492','11780872338','10267068828','11780825537','11780854896','10932719937','11780821730','10939187129','11441273476','11674409336','11674430435','11780800816','10939189064','10917222832','11780839385','10935179274','11674210366','11441173087','11674230436','10266735312','11674047511','11674044754','11674042461','11674103028','10266680891','11674034996','11441300513','10116982526','11673794092','11673721420','10266547138','11673496433','10917020693','11054877972','12434294048','11673327837','11673297648','11673291994','11673296514','11441323910','12171320996','11441277286','11672582814','11149134683','11441264212','11671847645','11270147023','11270147823','11509243696','11671843352','11441337542']

		if self.uploaddata.clean_csv() == False:
			print u'清理文件失败'
			# self.errorlog('清理文件失败')
			return False

		tmpCategorys = []
		for itemId in goodsItems:
			tmpCategorys.append({'keyword': itemId})
		i = 0
		for category in tmpCategorys:
			i = i + 1
			print i, category['keyword']
			self.goods_category(category)



	# 一次性上传所有数据
	def upload_json_whole(self):
		return self.uploaddata.upload_json_whole()



	# 获取需要采集的商品ID
	def get_items(self):
		r = requests.get(self.get_items_host)
		print r
		items = r.json()
		return items



def main(options):
	jd = GoodSpider()
	print u'采集开始'
	# jd.infolog('采集开始')
	if not jd.jd_login():
		return

	# if options.good > 0:
	# 	print '--------'
	# 	print options.good
	# 	print '--------'
	# 	tmp = {'keyword': options.good}
	# 	# jd.goods_category(tmp)
	# return

	jd.category_list()
	print u'采集结束'
	# jd.infolog(u'采集结束')
	print u'开始上传数据'
	# jd.infolog(u'开始上传数据')
	jd.upload_json_whole()
	print u'上传数据结束'
	# jd.infolog(u'上传数据结束')


if __name__ == '__main__':
	# help message
	parser = argparse.ArgumentParser(description='根据商品ID来采集商品信息')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-g', '--good', type=int, 
						help='京东商品ID', default=0)


	options = parser.parse_args()
	print options
	main(options)