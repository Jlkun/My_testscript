



#抽奖算法
import random
day_min =10  #日下限
day_max =100   #日上限
user_benfits_num =500   #用户贡献用于抽奖的钱
period=30  # 权益周期天数
draw_times=1 #每天能抽奖的次数
user_remain_num = period * day_min * draw_times
print("用户预留部分金额 user_remain_num = "+str(user_remain_num))

user_pool_num=(user_benfits_num-(period*day_min * draw_times))
print("用户往奖池放入总金额 user_pool_num= "+str(user_pool_num))

pool_total_remain_num =user_pool_num
# pool_total_remain_num =user_pool_num
print("总奖池目前剩余金额 pool_total_remain_num = "+str(pool_total_remain_num))

# userPack=(max(day_min,random.uniform(0,min(day_max,pool_total_remain_num/2))))
# print(min(day_max,pool_total_remain_num/2))
# redpack0=random.uniform(0,min(day_max,pool_total_remain_num/2))
# redpack1=round(redpack0redpack0,1)
redpack1=round(random.uniform(0,min(day_max,pool_total_remain_num/2)),1)
print("用户抽取到红包值为 userPack="+str((max(day_min,redpack1))))


user_remain_num=2.9
pool_total_remain_num=1.4
redpack1=round(random.uniform(0,min(day_max,pool_total_remain_num/2)),1)
print("用户抽取到红包值为 userPack="+str((max(day_min,redpack1))))


user_remain_num=2.8
pool_total_remain_num=0.9
redpack1=round(random.uniform(0,min(day_max,pool_total_remain_num/2)),1)
print("用户抽取到红包值为 userPack="+str((max(day_min,redpack1))))


user_remain_num=2.7
pool_total_remain_num=0.6
redpack1=round(random.uniform(0,min(day_max,pool_total_remain_num/2)),1)
print("用户抽取到红包值为 userPack="+str((max(day_min,redpack1))))


user_remain_num=2.6
pool_total_remain_num=0.6
redpack1=round(random.uniform(0,min(day_max,pool_total_remain_num/2)),1)
print("用户抽取到红包值为 userPack="+str((max(day_min,redpack1))))

user_remain_num=2.5
pool_total_remain_num=0.6
redpack1=round(random.uniform(0,min(day_max,pool_total_remain_num/2)),1)
print("用户抽取到红包值为 userPack="+str((max(day_min,redpack1))))

user_remain_num=2.4
pool_total_remain_num=0.4
redpack1=round(random.uniform(0,min(day_max,pool_total_remain_num/2)),1)
print("用户抽取到红包值为 userPack="+str((max(day_min,redpack1))))