# PyAPISSHTunnel

ローカルネットワーク内のAPIを一時的に外部の特定サーバ(SSH接続可能サーバ)に対して公開するためのツール
ngrokやssh -R ～～～のようなもの(プロキシ環境対応)

## 使い方

- config.json.sample -> config.json
- nginx-proxy.conf.sample  - > nginx-proxy.conf

に変換し中身を埋める
起動中は外部サーバにログイン中のみトンネルが生成され内部APIが叩けるようになる

SSHが鍵認証の場合はkeyディレクトリに配置

