import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def load_data(file_path):
    """CSVファイルを読み込み、特徴量とターゲットに分割する。"""
    game_data = pd.read_csv(file_path)
    X = game_data.drop("draw_card", axis=1)
    y = game_data["draw_card"].astype(int)
    return X, y

def evaluate_model(model, X_test, y_test):
    """モデルの精度を計算し、表示する。"""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"モデルの精度: {accuracy:.2f}")
    return accuracy

def predict_new_data(model, new_data):
    """新しいデータで推論を行う。"""
    prediction = model.predict(new_data)
    return "引く" if prediction[0] else "引かない"

if __name__ == "__main__":
    file_path = "../npc_style_data/npc_style_data.csv"
    model_path = "random_forest_model.pkl"

    # モデルのロード
    model = joblib.load(model_path)
    
    # データの読み込みと分割
    X, y = load_data(file_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # モデルの評価
    evaluate_model(model, X_test, y_test)

    # 推論の例
    new_data = pd.DataFrame([{
        "score_difference": 5,
        "player_burst_prob": 0.25,
        "opponent_burst_prob": 0.15,
        "remaining_cards_num": 8,
        "round": 2,
        "player_life": 3,
        "opponent_life": 2
    }])

    result = predict_new_data(model, new_data)
    print(f"推論結果: {result}")
