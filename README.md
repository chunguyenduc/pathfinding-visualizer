# pathfinding-visualizer
Simple Pathfinding Visualizer made from Python Tkinter

# Hướng dẫn sử dụng
- Kéo ô trắng để tạo wall
- Kéo ô tường để xóa tường
- Ô xanh lá là điểm bắt đầu, ô cam là điểm kết thúc. Kéo 2 ô để di chuyển vị trí

![](image/drag.gif)

- Chọn thuật toán, click Run để chạy
- Click Clear Path để xóa đường đi cũ
- Click Clar All để xóa hết tất cả
(Trong lúc chạy vẫn có thể Clear Path và Clear All được, nhưng Run thì không)

![](image/run.gif)

# Nhận xét
- Astar Search: Mở các nút hướng tới điểm kết thúc (Đo bằng Mahattan thì mở vuông hơn)

![alt text](image/Mahattan.png)	
![alt text](image/Euclide.png)


- Dijkstra Search: Mở các nút theo hình tròn
![alt text](image/Dijkstra.png)


- Breadth First Search: Mở các nút theo hình vuông
![alt text](image/BFS.png)


- Depth First Search: Mở 1 nút cho tới chết rồi lặp lại
![alt text](image/DFS.png)

# Ưu điểm
- GUI thân thiện, dễ xài.
- Visualize được nhiều thuật toán.

# Nhược điểm
- Code dơ, chưa tối ưu.
- Code phần chạy chưa mượt nên chạy nhiều lần sẽ bị chậm.
- Không đẹp bằng mấy cái trên mạng.

# Kết luận:
Nên xài Pygame hơn là Tkinter, vì lần đầu làm GUI nên không nghĩ là phần đồ họa lại quá khó như vậy.

# Dự định
Nếu mà siêng thì sẽ thêm chỉnh tốc chạy, chỉnh kích thước board, v.v..

