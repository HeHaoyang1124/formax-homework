/*
 * 代码来源：博客园 https://www.cnblogs.com/helloylh/p/17209739.html
 * 算法说明：本页代码使用的是A*启发式算法
 * 注释说明：本页代码保留了作者原有的格式化风格，
 *         原作者完全使用单行注释，我使用多行注释区分开来与原作者的注释
 */
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
 
const int ROW = 10;
const int COL = 10;
const int ZXDJ = 10;	//直线代价
const int XXDJ = 14;	//斜线代价
enum Dir { p_up, p_down, p_left, p_right, p_lup, p_ldown, p_rup, p_rdown };
struct Mypoint
{
	int row;
	int col;
	int f, g, h;
	bool operator==(const Mypoint& pos)
	{
		return (pos.row == row && pos.col == col);
	}
	void GetH(const Mypoint& Begpos, const Mypoint& Endpos)
	{
		int x = abs(Begpos.col - Endpos.col);//计算水平差距
		int y = abs(Begpos.row - Endpos.row);//计算垂直差距
		h = x + y;//计算总的差距
	}
	inline void GetF()
	{
		f = g + h;//计算f
	}
};
 
//树结构存储节点
struct TreeNode
{
	Mypoint pos;//当前点坐标
	TreeNode* pParent;//当前点的父节点
	vector<TreeNode*> pChild;	//存储当前点的所有孩子节点
	//构造函数
	TreeNode(const Mypoint& pos)
	{
		this->pos = pos;
		pParent = nullptr;
	}
};

/*
 * @brief 在当前位置，判断是否可以到达剩下八个方向的点
 *
 * 如果越界，则不能走
 * 如果是墙，则不能走
 * 如果已经走过，则不走
 * 否则能走
 *
 * @param map 地图，1表示墙，0表示路径
 * @param vis 标记有没有走过
 * @param pos 下一步到达点坐标
 * @return bool 是否能走
 */
//判断某个点能否走
bool CanWalk(int map[ROW][COL], bool vis[ROW][COL], const Mypoint& pos)
{
	//如果越界，不能走
	if (pos.row < 0 || pos.col < 0 || pos.row >= ROW || pos.col >= COL)
	{
		return false;
	}
	//如果是墙，不能走
	if (map[pos.row][pos.col])
	{
		return false;
	}
	//如果已经走过，不能走
	if (vis[pos.row][pos.col])
	{
		return false;
	}
	return true;//否则能走
}
 
int main()
{
	//地图，1表示墙，0表示路径
	int map[ROW][COL] =
	{
		{0,0,0,0,1,0,0,0,0,0},
		{0,0,0,0,1,0,0,0,0,0},
		{0,0,0,1,1,0,1,0,0,0},
		{0,0,0,0,1,0,1,0,0,0},
		{0,0,0,0,1,0,1,0,0,0},
		{0,0,1,0,1,0,0,0,0,0},
		{0,0,0,0,1,0,0,0,0,0},
		{0,0,0,0,0,0,1,0,0,0},
		{0,0,0,0,1,1,0,0,0,0},
		{0,0,0,0,1,0,0,0,0,0},
	};
 
	//起始点和终点
	Mypoint Begpos = { 1,1 };
	Mypoint Endpos = { 6,5 };
 
	//标记有没有走过
	bool vis[ROW][COL] = { false };
 
	//创建树根，即根节点
	TreeNode* pRoot = new TreeNode(Begpos);
 
	vector<TreeNode*> buff;	//存储孩子节点的数组
 
	TreeNode* pCurrent = pRoot;	//记录当前点
	TreeNode* pTemp = nullptr;	//试探节点,用于试探下一个位置的点
 
	bool isFindEnd = false;//终点标记
 
	//开始寻路
	/*
	 * A*算法步骤：
	 * 简单来说，本体是一个bfs算法，区别在于的不是从队头开始取
	 * 而是从队列（作者这里是vector数组存储的）中最小的代价点作为当前点进行扩展
	 * 其实使用优先队列优化效率更高
	 *
	 * 1. 依次试探八个方向是否能走计算g代价
	 * 2. 保留能走的点，存储在buff数组中
	 * 3. 在buff数组中找到最小代价点，作为下一步拓展点，同时出队列（删除数组元素）
	 * 4. 剩下还是bfs的那一套，直到判断终点（或者已经全部出队列表示死路一条）
	 */
	while (1)
	{
		//1. 某个点八个方向依次遍历 计算g代价
		for (int i = 0; i < 8; ++i)
		{
			//确定试探点的属性
			pTemp = new TreeNode(pCurrent->pos);
			//八个方向进行试探！
			switch (i)
			{
				//直线代价
			case p_up://上
				pTemp->pos.row--;
				pTemp->pos.g += ZXDJ;
				break;
			case p_down://下
				pTemp->pos.row++;
				pTemp->pos.g += ZXDJ;
				break;
			case p_left://左
				pTemp->pos.col--;
				pTemp->pos.g += ZXDJ;
				break;
			case p_right://右
				pTemp->pos.col++;
				pTemp->pos.g += ZXDJ;
				break;
				//斜线代价
			case p_lup://左上
				pTemp->pos.row--;
				pTemp->pos.col--;
				pTemp->pos.g += XXDJ;
				break;
			case p_ldown://左下
				pTemp->pos.row++;
				pTemp->pos.col--;
				pTemp->pos.g += XXDJ;
				break;
			case p_rup://右上
				pTemp->pos.row--;
				pTemp->pos.col++;
				pTemp->pos.g += XXDJ;
				break;
			case p_rdown://右下
				pTemp->pos.row++;
				pTemp->pos.col++;
				pTemp->pos.g += XXDJ;
				break;
			}
			//判断他们能不能走，能走的计算h及f 入树  存储在buff数组
			if (CanWalk(map, vis, pTemp->pos))
			{	//能走
				//计算代价
				pTemp->pos.GetH(pTemp->pos, Endpos);//计算h代价
				pTemp->pos.GetF();//得到最后的f代价，f=g+h 
				//把能走的这个点存入树中
				pCurrent->pChild.push_back(pTemp);//pTemp表示的就是下一个能走的点
				pTemp->pParent = pCurrent;//父子关系确定
				//存入数组
				buff.push_back(pTemp);
				//标记这个点走过
				vis[pTemp->pos.row][pTemp->pos.col] = true;
			}
			else
			{
				//不能走则删除pTemp，继续遍历下一个方向的点
				delete pTemp;
				pTemp = nullptr;
			}
		}
		/*
		遍历完八个方向后，找到最小代价点，并且移动，然后删除
		*/
		auto itMin =  min_element(buff.begin(), buff.end(), [&](TreeNode* p1, TreeNode* p2)
			{
				return p1->pos.f < p2->pos.f;
			});
		
		//当前点移动到这个最小代价点
		pCurrent = *itMin;
		//删除最小代价节点
		buff.erase(itMin);
 
		//有没有到达终点
		if (pCurrent->pos == Endpos)
		{
			isFindEnd = true;
			break;
		}
		//没有终点，自然一直删除节点，则buff为空
		if (buff.size() == 0)
		{
			break;
		}
	}
 
	if (isFindEnd)
	{
		cout << "找到终点了!\n";
		while (pCurrent)
		{
			cout << "(" << pCurrent->pos.row << "," << pCurrent->pos.col << ")";
			pCurrent = pCurrent->pParent;
		}
	}
	else
	{
		cout << "没有找到终点!\n";
 
	}
	return 0;
}