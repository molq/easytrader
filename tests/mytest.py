import easytrader

# 1. 创建交易客户端
user = easytrader.use("xq")  # 雪球
# user = easytrader.use('ht_client')  # 华泰

# 2. 登录/连接
# user.prepare("../config.json")
# 或 user.connect('client_path')

# 3. 执行交易
# user.buy("000001", price=10.0, amount=100)

# 4. 创建跟单策略
follower = easytrader.follower(platform="xq")
follower.login(
    cookies="cookiesu=661760411130159; device_id=8fc5b1eaa2f27255f3a57e733348dad7; smidV2=20251014110531131e693cfdee3bae60bbd164c8525108003d1aa9354a0c590; s=ab1o4yamzq; Hm_lvt_1db88642e346389874251b5a1eded6e3=1760411131,1762247791,1762508680; HMACCOUNT=9E10F8B43ADD912D; remember=1; xq_a_token=956206e2f2bc462784e9ea0c5ba034993af9a781; xqat=956206e2f2bc462784e9ea0c5ba034993af9a781; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjU5NzQ3MTIxMTUsImlzcyI6InVjIiwiZXhwIjoxNzY1MTAwNzA3LCJjdG0iOjE3NjI1MDg3MDczMDgsImNpZCI6ImQ5ZDBuNEFadXAifQ.TvS2EN3oN1EosuBE29N2-s4yCTln5lcyLjC_2Bm_N7pH_hEr7lmMLjEEKNDsY6XWOlTTeSybA61sY2hA7tQf2TJGE3lu0a9RHIun-rqegoLEEoQx020aGYXka4D4-Iv8_JwjLSaoMesMx0w4DAD0r3pxsFlOLshZx0KqK50gJuzJZs0RexxuOHMgLx_-uxvuNK2WYEvXMGTUebkArVi9CkI5nNTg0qRgCZYCksb-a6z-w38zV-JohL5SC204895PQ-NUd6bzE3pGS2ZfxYx27dkf9jChPsft3EH16dtU9yKy90ze_DcdleqPPeE3UAlQDizhPJSCSHMESWpj5Aopkg; xq_r_token=666d0ff6146d8a919afd7385ef12a3b9ead1121c; xq_is_login=1; u=5974712115; bid=71e7421c8bdd04512ff569539a2640a6_mhoo6kkt; __utmc=1; __utmz=1.1762508716.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); acw_tc=3ccdc15217629478976328112e596972f53e0fc7f991d78d01a9a6be3a9857; is_overseas=0; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=E5osJyLm2+miOPNGrSzfo2GciYhidX5iAwG0qiQ71CuCQVBx2kYKUfBN1/cj+8Sc0Ay3MiBAVu7SrMldNKsJJQ%3D%3D; __utma=1.1586223490.1762508716.1762508716.1762949643.2; __utmt=1; __utmb=1.1.10.1762949643; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1762949684; ssxmod_itna=1-Qqf20KDKYvqAxYqYQiQLPAjmeTpDuDUx0dGM0Deq7tDRDFqAPYDHKIEC75E4NGFCnDDtqlr80tDlrh0YDSxD=7DK4GTwGgi7_154pGDT3dhe8xprqFmYEi5tbfI6kBjOLKbMy2HLXzbUiqGImDG2DYoDCqDS0DD9KrArDYAfDBYD74G_DDeDiObDGdW52DDFBjRQMWiQFW45geDE0YrF0DDgRPD1b1nbgWi3iPGfbWpi2AiDbMwp2GPtx0fCaOODzdrDboodX/8Dtq7PdCINPpWQnt6MB_dYmmGpKG4hD3h_C7mYBh433MxwB4eD4cLQM7ex3hwiidn1Mw457ezdCwdrpdbMYeorz9xiwYQoBd_m43m5/DYqOD4rYbmDHBxhD4eehViDD; ssxmod_itna2=1-Qqf20KDKYvqAxYqYQiQLPAjmeTpDuDUx0dGM0Deq7tDRDFqAPYDHKIEC75E4NGFCnDDtqlr80YD==32YIts9jop1Z/PlDrh4Neck4xD"
)
follower.follow(users=user, strategies=["ZH3542839"], initial_assets=1000000)
