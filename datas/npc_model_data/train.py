import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def load_data(file_path):
    """CSVファイルを読み込み、特徴量とターゲットに分割する。"""
    game_data = pd.read_csv(file_path)
    X = game_data.drop("draw_card", axis=1)
    y = game_data["draw_card"].astype(int)  # 0: 引かない, 1: 引く
    return X, y

def train_model(X_train, y_train, model_path="random_forest_model.pkl"):
    """ランダムフォレストモデルを訓練し、保存する。"""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, model_path)
    print(f"モデルの訓練が完了し、{model_path} に保存されました。")
    return model

if __name__ == "__main__":
    file_path = "../npc_style_data/npc_style_data.csv"
    
    # データの読み込みと分割
    X, y = load_data(file_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # モデルの訓練
    train_model(X_train, y_train)
