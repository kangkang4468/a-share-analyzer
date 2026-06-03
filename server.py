import http.server
import socketserver
import json
import os

PORT = 8000
FAV_FILE = "favorites.json"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/save_favorites':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                # 解析前端传来的 JSON
                favorites = json.loads(post_data.decode('utf-8'))
                
                # 写入本地 favorites.json
                with open(FAV_FILE, 'w', encoding='utf-8') as f:
                    json.dump(favorites, f, ensure_ascii=False)
                
                # 返回成功响应
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            except Exception as e:
                print(f"Error saving favorites: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    # 切换工作目录到脚本所在目录，确保可以正常读取 HTML 和 JSON
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # 允许重复绑定端口
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print("================================================================")
        print(f" 本地服务已启动！")
        print(f" 请在浏览器中打开: http://localhost:{PORT}/stock_analysis.html")
        print(" (在前端页面的自选股拖拽和删除操作将自动保存到 favorites.json)")
        print("================================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已关闭")
