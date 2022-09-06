from atoolbox import FileHandler
import pandas as pd

f = FileHandler("feature_data.pkl", subdir=["data"])
df = pd.DataFrame(f.read())

# remove constants
df = df.loc[:, (df != df.iloc[0]).any()]

# Reset index
df.set_index("trai", inplace=True)

# remove enumerations
df2 = df.diff().round(3).iloc[1:-1]
df = df.loc[:, (df2 != df2.iloc[1]).any()]

# min max scale
df = (df - df.min()) / (df.max() - df.min())

app = QtWidgets.QApplication(["test"])
FRF_Analyzer = QtWidgets.QMainWindow()
# print('Run GUI\n')
ui = Ui_FRF_Analyzer(df)
ui.setupUi(FRF_Analyzer)
FRF_Analyzer.show()
sys.exit(app.exec_())
