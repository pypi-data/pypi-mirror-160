

data = pd.read_csv("data/After2005.csv")
data = data.drop(['Unnamed: 0'], axis=1)




def LookUp(CIK, DateFiled, Type = '10Q'):
    prefix = 'https://www.sec.gov/Archives/edgar/'
    return prefix + data.loc[(data.CIK == CIK) & (data.DateFiled == DateFiled), :].TXTAddress


