#!/usr/bin/python3
"""
BW/BW2 Seed Filter のexeファイル作成スクリプト
"""

import subprocess
import sys
import os

def build_exe():
    """exeファイルを作成する"""
    print("exeファイルを作成中...")
    
    # specファイルが存在する場合はそれを使用
    if os.path.exists("BW2_Seed_Filter.spec"):
        print("specファイルを使用してビルドします...")
        cmd = ["pyinstaller", "BW2_Seed_Filter.spec"]
    else:
        print("specファイルが見つからないため、基本的な設定でビルドします...")
        # 基本的なPyInstallerコマンド
        cmd = [
            "pyinstaller",
            "--onefile",  # 単一のexeファイルにまとめる
            "--windowed",  # コンソールウィンドウを表示しない
            "--name=BW2_Seed_Filter",  # exeファイルの名前
            "--add-data=file;file",  # fileフォルダを含める
            "--add-data=snivy_generator;snivy_generator",  # snivy_generatorフォルダを含める
            "--add-data=trainer_skips;trainer_skips",  # trainer_skipsフォルダを含める
            "--hidden-import=drilbur_filter",
            "--hidden-import=tepig_filter",
            "--hidden-import=trainer_skips.TSkipWindow",
            "main.py"
        ]
        
        # アイコンファイルが存在する場合は追加
        if os.path.exists("kyurem-white.png"):
            cmd.extend(["--icon=kyurem-white.png"])
    
    try:
        subprocess.check_call(cmd)
        print("exeファイルの作成が完了しました！")
        print("dist/BW2_Seed_Filter.exe にファイルが作成されました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"exeファイルの作成に失敗しました: {e}")
        return False
    except FileNotFoundError:
        print("PyInstallerが見つかりません。")
        return False

def clean_build_files():
    """ビルド時に作成された一時ファイルを削除する"""
    print("一時ファイルを削除中...")
    dirs_to_remove = ["build", "__pycache__"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                import shutil
                shutil.rmtree(dir_name)
                print(f"{dir_name} フォルダを削除しました")
            except Exception as e:
                print(f"{dir_name} フォルダの削除に失敗: {e}")

def main():
    """メイン関数"""
    print("BW/BW2 Seed Filter - exeファイル作成ツール")
    print("=" * 50)
    
    # exeファイルを作成
    if build_exe():
        print("\n成功！exeファイルが作成されました。")
        print("distフォルダ内のBW2_Seed_Filter.exeを配布してください。")
        
        # 一時ファイルの削除を確認
        response = input("\nビルド時に作成された一時ファイルを削除しますか？ (y/n): ")
        if response.lower() in ['y', 'yes', 'はい']:
            clean_build_files()
    else:
        print("\n失敗！exeファイルの作成に失敗しました。")

if __name__ == "__main__":
    main() 