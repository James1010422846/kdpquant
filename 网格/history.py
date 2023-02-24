
class History:
    """买入操作历史类"""
    # 操作 1 买入 -1 卖出
    stock_code = ""
    count = 0
    price = 0.0
    opt_type = 0

    def __init__(self, stock_code, opt_type, price, count):
        self.stock_code = stock_code
        self.opt_type = opt_type
        self.price = price
        self.count = count


# 最大值中的最大值
max = data['high'].max()
min = data['low'].min()
# 基准价
benchmark = float(Decimal((max + min) / 2 * 1.2).quantize(Decimal('0.000')))
print(max, min, benchmark)

grid = 0.05
count = 100
max_consume_money = Decimal(0)
consume_money = Decimal(0)
opt = []
# [日期, 价格, -1/1] 用于画点
# 历史
opt_b = []
opt_s = []
# 总利润
profit = 0


# 建仓
first = data.iloc[0]
while benchmark * (1 - grid) >= first['open']:
    # 一手买入 或者 倍数买入
    # 买入
    # 基准价变更
    benchmark = float(Decimal(benchmark * (1 - grid)).quantize(Decimal('0.000')))
    print(data.index[0], "建仓买入", benchmark)

    # 计算的操作
    consume_money += Decimal(benchmark) * Decimal(count)

    # 添加记录
    h = history.History(stock_code, 1, benchmark, count)
    opt.append(h)
    opt_b.append([data.index[0], benchmark, 1])


df_b = pd.DataFrame(opt_b, columns=['timestamp', 'price', 'opt'])
df_b.set_index('timestamp', drop=True, inplace=True)
df_b.sort_index()

df_s = pd.DataFrame(opt_s, columns=['timestamp', 'price', 'opt'])
df_s.set_index('timestamp', drop=True, inplace=True)
df_s.sort_index()

plt.plot(df_b.index, df_b['price'], 'or')
plt.plot(df_s.index, df_s['price'], 'og')

plt.show()
