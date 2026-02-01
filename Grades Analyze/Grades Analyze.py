import numpy as np
import matplotlib.pyplot as plt


class GradesReader:
    """
    考试成绩读取与分析类
    功能：读取CSV成绩文件、处理缺失值、可视化总分分布
    CSV文件格式（示例）：学生编号,专业课1,专业课2,专业课3,专业课4,总分
    """
    def __init__(self, filename):
        self.filename = filename
        try:
            self.grades = np.genfromtxt(filename, delimiter=',',dtype=float)
        except FileNotFoundError:
            print("Error: File not found")
            self.grades = None
        except ValueError:
            print("Error: File format is not correct")
            self.grades = None
        except Exception as e:
            print(e)
            self.grades = None

    def nan_solve(self):
        """
        缺失值处理方法：遍历每一列，用该列非缺失值的均值填充NaN
        处理逻辑：先判断数据是否有效，再逐列检测缺失值，有则填充
        """
        if self.grades is None:
            print("No Grades Found")
            return
        for i in range(self.grades.shape[1]):
            temp=self.grades[:,i]
            nan_count=np.count_nonzero(temp!=temp)
            if nan_count!=0:
                temp_not_nan=temp[temp==temp]
                temp[np.isnan(temp)]=np.mean(temp_not_nan)
                self.grades[:,i]=temp

    def __get_avg_total_grade(self):
        """
        私有方法（仅类内部调用）：计算所有学生的总分平均分
        私有方法命名规则：以双下划线开头，外部无法直接调用
        :return: float类型的总分平均分，数据无效时返回None
        """
        if self.grades is None:
            print("No grades found")
            return None
        if self.grades.shape[1] < 6:
            print("Error: No total grade column (index 5) found")
            return None
        total_grades=self.grades[:,5]
        return total_grades.mean()

    def plot_scatter(self):
        """
        可视化方法：绘制学生编号与总分的散点图
        图表包含：散点、坐标轴标签、标题、平均分参考线、图例，最终保存为图片
        """
        if self.grades is None:
            print("No Grades Found")
            return
        x=self.grades[:,0]
        y=self.grades[:,5]
        plt.figure(figsize=(10,10))
        plt.scatter(x,y,color='red',alpha=0.5,s=100)
        plt.title("Scores of The Exam")
        plt.xlabel('Student Number')
        plt.ylabel('Total Grade')
        plt.xticks(np.arange(x.min(),x.max()+1,5))
        plt.yticks(np.arange(y.min(),y.max()+1,5))
        plt.axhline(
            y=self.__get_avg_total_grade(),
            color='black',
            linestyle='-',
            linewidth=2,
            label=f"Average Total Grade: {self.__get_avg_total_grade():.2f}"
        )
        plt.legend()
        plt.savefig('Grades.png')
if __name__ == '__main__':
    reader = GradesReader('TEST.csv')
    reader.nan_solve()
    reader.plot_scatter()
