# 导入必要的模块
import pgzrun  # 导入pgzrun模块，用于制作游戏
import random  # 导入random模块，用于随机打乱题目顺序

# 定义窗口宽度和高度
WIDTH = 1280  # 设置游戏窗口的宽度为1280像素
HEIGHT = 720  # 设置游戏窗口的高度为720像素

# 设置窗口标题
TITLE = '2025我的世界最强玩家挑战大会专业程序'  # 设置游戏窗口的标题

# 定义游戏中的三种矩形框：问题框、计时器框、四个答案框
problem_box = Rect(50, 40, 820, 240)  # 问题显示区域的矩形框
timer_box = Rect(990, 40, 240, 240)  # 计时器显示区域的矩形框
answer_box1 = Rect(50, 360, 500, 165)  # 第一个答案选项的矩形框
answer_box2 = Rect(730, 360, 500, 165)  # 第二个答案选项的矩形框
answer_box3 = Rect(50, 540, 500, 165)  # 第三个答案选项的矩形框
answer_box4 = Rect(730, 540, 500, 165)  # 第四个答案选项的矩形框

# 将四个答案框放入一个列表中
answer_boxes = [answer_box1, answer_box2, answer_box3, answer_box4]  # 方便后续统一处理四个答案框

# 打开文件并读取问题
with open('我的世界问题库.txt', 'r', encoding='utf-8') as f:  # 以只读方式打开题库文件，编码为utf-8
    content = f.readlines()  # 将读取的每一行内容存放在content列表中

# 建立问题的空列表
questions = []  # 用于存放所有题目的列表

# 将每行数据转换为列表
for q in content:  # 遍历题库文件的每一行
    questions.append(eval(q))  # 用eval将字符串转换为列表，并添加到questions中

# 打乱列表，随机出题
random.shuffle(questions)  # 随机打乱题目的顺序

# 弹出第一个问题，开始游戏
question = questions.pop(0)  # 从题目列表中取出第一个题目作为当前题目

# 剩余时间
time_left = 10  # 每道题的答题时间为10秒

# 初始化得分
score = 0  # 初始分数为0

# 绘制函数
def draw():  # 游戏界面的绘制函数，每帧自动调用
    # 绘制游戏界面
    screen.fill("black")  # 填充背景为黑色
    screen.draw.filled_rect(problem_box, "white")  # 绘制问题框，填充为白色
    screen.draw.filled_rect(timer_box, "white")  # 绘制计时器框，填充为白色
    for box in answer_boxes:  # 遍历四个答案框
        screen.draw.filled_rect(box, "white")  # 绘制每个答案框，填充为白色

    # 绘制计时器文字
    screen.draw.textbox(str(time_left), timer_box,
                        fontname='fusion-pixel', color=("black"))  # 在计时器框中显示剩余时间

    # 绘制问题文字
    screen.draw.textbox(question[0], problem_box,
                        fontname='fusion-pixel', color=("black"))  # 在问题框中显示题目内容

    # 绘制四个选项框中的文字
    i = 1  # 选项从question[1]开始
    for box in answer_boxes:  # 遍历四个答案框
        screen.draw.textbox(question[i], box, fontname='fusion-pixel', color=("black"))  # 在答案框中显示选项内容
        i += 1  # 选项索引加1

# 回答正确
def get_correct_answer():
    global question, score, time_left  # 声明全局变量，便于在函数内修改
    score += 1  # 得分加1
    # 判断问题列表是否为空
    if questions:  # 如果还有剩余题目
        time_left = 10  # 剩余时间重置为10秒
        question = questions.pop(0)  # 取出下一个题目
    else:
        game_over()  # 没有题目了，游戏结束

# 游戏结束
def game_over():
    global question, time_left  # 声明全局变量
    message = f"游戏结束\n挑战成功 {score} 题"  # 生成游戏结束提示信息
    question = [message, "-", "-", "-", "-", 5]  # 用特殊格式重置当前题目，防止报错
    time_left = 0  # 剩余时间归零

# 检测鼠标按键
def on_mouse_down(pos):  # 鼠标点击事件处理函数，参数pos为鼠标点击的位置
    choice = 1  # 选项编号从1开始
    for box in answer_boxes:  # 遍历四个答案框
        if box.collidepoint(pos):  # 如果鼠标点击在当前答案框内
            # 判断是否回答正确
            if question[5] == choice:  # question[5]存储正确答案的编号
                sounds.yes.play()  # 播放回答正确的音效
                get_correct_answer()  # 进入下一个题目
            else:
                sounds.lose.play()  # 播放回答错误的音效
                music.stop()  # 停止背景音乐
                game_over()  # 回答错误，游戏结束
        choice += 1  # 选项编号加1

# 时间更新函数
def update_time():  # 每秒调用一次，更新剩余时间
    global time_left
    if time_left:  # 如果还有剩余时间
        time_left -= 1  # 剩余时间减1秒
    else:
        game_over() # 时间为0，游戏结束

# 定时器，每秒钟调用一次update_time函数
clock.schedule_interval(update_time, 1)  # 每隔1秒自动调用一次update_time函数

# 播放背景音乐
music.play('superbrain')  # 播放背景音乐文件superbrain.mp3

# 运行游戏
pgzrun.go()  # 启动游戏主循环

