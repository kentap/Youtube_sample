import os
import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
import requests
import json
import boto3
from langchain_community.chat_models import BedrockChat
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# APIキーとYouTube APIクライアントの設定
api_key = 'your youtube api key'
api_service_name = 'youtube'
api_version = 'v3'
youtube = build(api_service_name, api_version, developerKey=api_key)


# Streamlitアプリケーションの設定
st.title("YouTubeの動画情報分析")

# 検索キーワードの入力
search_word = st.text_input("検索ワード")

# 実行回数の選択
nums = st.selectbox("何回実行する？実行回数×5件分のデータが取得できます", [i for i in range(1, 21)], index=0)

# データフレームの初期化
# セッションステートの初期化
if 'df_output' not in st.session_state:
    st.session_state.df_output = pd.DataFrame()  # 初期値を設定

final_data = pd.DataFrame()
df_output = pd.DataFrame() 

# APIを実行する関数
def execute_api(search_word, nums):
    result_list = []

    request = youtube.search().list(q=search_word, part='snippet', type='video', order='viewCount')
    get_response = request.execute()

    for _ in range(nums):
        result_list += get_response['items']
        request = youtube.search().list_next(request, get_response)
        get_response = request.execute()

    data = pd.DataFrame(result_list)
    data2 = pd.DataFrame(list(data['id']))['videoId']
    data3 = pd.DataFrame(list(data['snippet']))[['channelTitle', 'publishedAt', 'channelId', 'title']]
    final_data = pd.concat([data2, data3], axis=1)

    return final_data

# 個別の動画ごとの統計情報を取得する関数
def get_statistics(video_id):
    statistics_data = youtube.videos().list(part='statistics', id=video_id).execute()['items'][0]['statistics']
    return statistics_data


# API実行ボタン
if st.button("API実行"):
    if search_word:
        final_data = execute_api(search_word, nums)
        df_static_data = pd.DataFrame(list(final_data['videoId'].apply(lambda x: get_statistics(x))))[
            ['viewCount', 'likeCount', 'commentCount']]
        st.session_state.df_output = pd.concat([final_data, df_static_data], axis=1)

        st.write("データの取得が完了しました。")
        
        st.write(st.session_state.df_output)
        
    
    else:
        st.warning("検索ワードを入力してください。")
   

#分析するボタン
if st.button("分析する"):
    if not st.session_state.df_output.empty:
        prompt = ChatPromptTemplate.from_template("{content}の内容を分析して、人気の動画の傾向について解説してください。")
        chat = BedrockChat(model_id="your model ID",model_kwargs={"temperature": 0.7})
        content =  st.session_state.df_output.to_csv(index=False, encoding='utf-8_sig') 
         
        chain = prompt | chat | StrOutputParser()

        analysis_result = chain.invoke({"content":content})
        st.write("分析結果:")
        st.write(analysis_result)
    else:
        st.warning("データがありません。先にAPIを実行してください。")


# 終了メッセージ
if st.button("終了"):
    st.write("プログラムを終了しました。")
