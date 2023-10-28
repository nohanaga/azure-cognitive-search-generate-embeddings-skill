---
page_type: sample
languages:
- python
products:
- azure
- azure-cognitive-search
- azure-cognitive-services
name: Generate Image Embeddings Custom Skill
urlFragment: azure-cognitive-search-generate-embeddings-skill
description: This custom skill enables 
---
# Generate Image Embeddings Custom Skill for Azure Cognitive Search
このカスタムスキルは、Azure AI services の Vectorize Image API を使用して画像をベクトル化します。

# Deployment

本スキルは、Azure AI services リソースが必要です。また、`COMPUTER_VISION_ENDPOINT` と `COMPUTER_VISION_KEY` が必要です。Azure Functions にデプロイする際は、**「アプリケーション設定」項目に設定する必要**があります。

## スキルのデプロイ方法
1. Azure portal で、Azure AI services リソースを作成します。
2. Azure AI services の API キーとエンドポイントをコピーします。
3. このレポジトリを clone します。
4. Visual Studio Code でレポジトリのフォルダを開き、Azure Functions にリモートデプロイします。
5. Functions にデプロイが完了したら, Azure Portal の Azure Functions の設定→構成から、`COMPUTER_VISION_ENDPOINT` と `COMPUTER_VISION_KEY` 環境変数にそれぞれ値を貼り付けます。


## Requirements

Azure Functions へデプロイする場合、以下が必要となります。

- [Visual Studio Code](https://azure.microsoft.com/products/visual-studio-code/)
- [Azure Functions for Visual Studio Code](https://learn.microsoft.com/azure/azure-functions/functions-develop-vs-code?tabs=node-v3%2Cpython-v2%2Cisolated-process&pivots=programming-language-python)

## Settings

この Funcsions は、有効な Azure AI services API キーが設定された `COMPUTER_VISION_KEY` の設定と、Azure AI services エンドポイント `COMPUTER_VISION_ENDPOINT` を必要とします。
ローカルで実行する場合は、プロジェクトのローカル環境変数で設定できます。これにより、API キーが誤ってコードに埋め込まれることがなくなります。
Azure Functions で実行する場合、これは「アプリケーションの設定」で設定できます。


## Sample Input:

カスタムスキルは画像の data 項目などを Azure Cognitive Search から受け取ります。data 項目には Base64 エンコードされた画像データが格納されているので、デコードして Python の バイナリストリームにロードします。

```json
{
    "values": [
        {
            "recordId": "record1",
            "data": { 
                "image": {
                    "$type": "file",
                    "data": "/9j/4AAQS...",
                    ...
                }
            }
        }
    ]
}
```

## Sample Output:

```json
{
    "values": [
        {
            "recordId": "record1",
            "embeddings": [0.6376953,2.2128906,...],
            "errors": {}
        }
    ]
}
```

## スキルセット統合の例

このスキルを Azure Cognitive Search パイプラインで使用するには、スキル定義をスキルセットに追加する必要があります。この例のスキル定義の例を次に示します（特定のシナリオとスキルセット環境を反映するように入力と出力を更新する必要があります）。

```json
{
    "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
    "name": "GenerateImageEmbeddingsSkill",
    "description": "Convert an image to a vector using the Vectorize Image API.",
    "uri": "[AzureFunctionEndpointUrl]/api/GenerateImageEmbeddings?code=[AzureFunctionDefaultHostKey]",
    "context": "/document/normalized_images/*",
    "inputs": [
        {
            "name": "image",
            "source": "/document/normalized_images/*"
        }
    ],
    "outputs": [
        {
          "name": "embeddings",
          "targetName": "embeddings"
        }
    ]
}
```

## インデクサー設定の例
インデクサーに出力フィールドのマッピングを設定します。これを行わないと、エンリッチ処理されたツリーから embeddings データを検索フィールドへマッピングすることができません。

```json
{
  "outputFieldMappings": [
    {
      "sourceFieldName": "/document/normalized_images/0/embeddings",
      "targetFieldName": "embeddings"
    }
  ],
}
```