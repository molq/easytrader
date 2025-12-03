import easytrader
from easytrader.log import logger

# 1. 创建交易客户端
# user = easytrader.use("xq")  # 雪球
# user = easytrader.use('ht_client')  # 华泰
user = easytrader.use('miniqmt')  # miniqmt
# 2. 登录/连接
# user.prepare("../config.json")
# 或 user.connect('client_path')

# user.connect(
#     miniqmt_path=r"D:\soft\国金证券QMT交易端\userdata_mini",  # QMT 客户端下的 miniqmt 安装路径
   
#     stock_account="8887670918",  # 资金账号
    
#     trader_callback=None   # 默认使用 `easytrader.miniqmt.DefaultXtQuantTraderCallback`
# )


user.connect(
    
    miniqmt_path=r"D:\国金QMT交易端模拟\userdata_mini",
    stock_account="62500888",  # 资金账号
    trader_callback=None   # 默认使用 `easytrader.miniqmt.DefaultXtQuantTraderCallback`
)
# 获取资金状况

logger.error("获取资金状况: %s", user.balance)

# 获取持仓

logger.error("获取资金获取持仓状况: %s", user.position)

# 3. 执行交易
# user.buy("000001", price=10.0, amount=100)

# 4. 创建跟单策略
follower = easytrader.follower(platform="xq")
follower.login(
    cookies="cookiesu=911741358545830; smidV2=20250307224226891d4776dee78eb8916ec6d39dccc26100de281ff8d605f20; device_id=5ba82b71970b271d37e98b61d26e8eae; s=bp134pqcwo; Hm_lvt_1db88642e346389874251b5a1eded6e3=1741358546,1742048088; u=5974712115; bid=71e7421c8bdd04512ff569539a2640a6_min9hua8; acw_tc=1a0c652117647725922116198ea5bc7f3f09b8cd7b1bd92880271442095025; remember=1; xq_a_token=64aca9edbac17928f087765e51a10f5ac84a5656; xqat=64aca9edbac17928f087765e51a10f5ac84a5656; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjU5NzQ3MTIxMTUsImlzcyI6InVjIiwiZXhwIjoxNzY3Mjc0MjEwLCJjdG0iOjE3NjQ3NzI2MTk4MzEsImNpZCI6ImQ5ZDBuNEFadXAifQ.NJdqZhoYBkbgCSyEdpb7ZoF3N6VlPE6AKPCd7fDR7SSv_M_T53MNyeojTIYbxba48iU4RqVxajdpgmFgCFQgCqJDLKadtbgDdhB1ArK8IE-Kd9_VDOkVI2gaUc1XwSvXtSqvMep-hT-otzd0bwMTPbT3VI7E1-T5KA0IeN_R0r3hQW8-J9Qx8SMgAKleDNZw9aqD3aFBGwkDAdvjxFIxAXpkScSbkMGXxU2qdR1hdVKrW1zGfYC-rEi2yZy0EkneAf7pWUCZnXdYItJEQIPuXEYYLMtsMQSGxt676CX9ZtnV1pfU9cPO2s8JFTL9tQK9upK9XSFEDlKAAHAYqgU3vg; xq_r_token=a30379137e3e11d0eaf8fb6eda6c8931f854e968; xq_is_login=1; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=FeAVeOoEXFkP/uhwBR37NcePjLKbDplQHuL4JjWiwIppyFaS8rIlmPpZYJp2z5NuciC6zjYkncNTK0OgpZiK5Q%3D%3D; _c_WBKFRo=2vlqk3EfftMIGBiu188PcEpzGgEbisnsnZNqm9yB; _nb_ioWEgULi=; acw_sc__v3=69304b1a9d45ff36243f9cbc0867e7662457b3e5; ssxmod_itna=1-iqRxR7qQqeqEG0CiDOii=DkAeiOeDXDULqiQGgADFqAPqDHWzOUADODUokD5HoTxDC4R0DYPyD05=iDnqD8jDQeDvD28iiD0Cdqt6HA27ExCe7DRGK6d5QG60xdOAaU8qoXeQTbcO7uGkDfGFBQ5xemekCOeDHxi8DBI4KroYDeeaDCeDQxirDD4DADibr4D11DDkD04AIIff_4GWDm4ADWPDYxDrGfoDRxxD0ZnwDQ9oG9wFwfPDBEpn81otk1dXN4C55sf4lRDqG4G1vD0HH7zuqszS8g3Xs5z6oEoDXONDvE85XKg2X7W08ac3=9ODGGrxxeH7o=YYeB=VDhMi=hEiYODQGYq0D8hxMBKoCmCxDirRrf2QD_MEN/gND4_P3m/emljmp0iSlp4r5rIw1nwsAD4ApK0iePnMQbqiDxD; ssxmod_itna2=1-iqRxR7qQqeqEG0CiDOii=DkAeiOeDXDULqiQGgADFqAPqDHWzOUADODUokD5HoTxDC4R0DYPGDDPYD0DfgTAt1RBItz/DbGOqEzO3D"
)
follower.follow(users=user, strategies=["ZH3381319"], initial_assets=100000)
