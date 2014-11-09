#include <iostream>
#include <algorithm>
#include <queue>
#include <thread>
#include <cassert>
#include <map>
#define mp make_pair
using namespace std;

struct point {
	int label;
	vector<double> cood;
};

#define K 2

int threads = 4;
int dimensions = 0;
vector<vector<pair<double,point*> > > closest_lists;
vector<point> points;

double dist(const point& x, const point& y){
	// cout<<"fuck"<<x.cood.size()<<" "<<y.cood.size()<<endl;
	assert(x.cood.size() == y.cood.size());
	double d = 0;
	for (int i=0; i<x.cood.size(); i++){
		d += (x.cood[i]-y.cood[i])*(x.cood[i]-y.cood[i]);
	}
	return d;
}

void closestK(vector<pair<double,point*> >& ans, int begin, int end, point p, int k){
	// cout<<"ck: "<<begin<<" "<<end<<endl;
	ans.clear();
	priority_queue<pair<double, point*> > heap;
	for (int i=begin; i<begin+k; i++){
		heap.push(mp(dist(p, points[i]), &points[i]));
	}
	for (int i = begin+k; i<=end; i++){
		double cd = dist(p, points[i]);
		auto e = heap.top();
		if (cd < e.first){
			heap.pop();
			heap.push(mp(cd, &points[i]));
		}
	}
	while (!heap.empty()){
		auto e = heap.top();
		heap.pop();
		ans.push_back(e);
	}
	reverse(ans.begin(), ans.end());
}

int aggregate(vector<pair<double,point*> >& closest_k){
	map<int, int> cnt;
	for (int i=0; i<closest_k.size(); i++){
		int lbl = closest_k[i].second->label;
		if (cnt.count(lbl)==0) cnt[lbl]=0;
		cnt[lbl]++;
	}
	int ml = -1;
	for (auto i = cnt.begin(); i!=cnt.end(); i++){
		if (ml==-1) {
			ml = i->first;
		} else {
			if (cnt[ml] < i->second){
				ml = i->first;
			}
		}
	}
	return ml;
}

void find_overall_closest_k(vector<pair<double, point*> >& ans, int k){
	priority_queue<pair<pair<double, point*>, pair<int,int> >, vector<pair<pair<double, point*>, pair<int,int> > >, greater<pair<pair<double, point*>, pair<int,int> > > > heap;
	for (auto i = closest_lists.begin(); i!=closest_lists.end(); i++){
		heap.push(mp(i->front(), mp(i-closest_lists.begin(),0)));
	}
	ans.clear();
	for (int i=0; i<k; i++){
		auto z = heap.top();
		ans.push_back(z.first);
		heap.pop();
		if (z.second.second+1 < closest_lists[z.second.first].size()){
			heap.push(mp(closest_lists[z.second.first][z.second.second+1], mp(z.second.first, z.second.second)));
		}
	}
}

void read_points(){
	points.clear();
	int n, d;
	cin>>n>>d;
	dimensions = d;
	for (int i=0; i<n; i++){
		point p;
		for (int j=0; j<d; j++){
			double a;
			cin>>a;
			p.cood.push_back(a);
		}
		cin>>p.label;
		points.push_back(p);
	}
}

void print(vector<pair<double, point*> > ck){
	cout<<"---------------\n";
	for (int i=0; i<ck.size(); i++){
		cout<<"dist: "<<ck[i].first<<endl;
		for (int j = 0; j<ck[i].second->cood.size(); j++){
			cout<<ck[i].second->cood[j]<<" ";
		}
		cout<<endl;
	}
	cout<<"---------------\n";
}

int answer_query(){
	point p;
	for (int i=0; i<dimensions; i++){
		double a;
		cin>>a;
		p.cood.push_back(a);
	}

	int k = 2;

	int chunk = points.size()/threads;
	closest_lists.clear();
	closest_lists.resize(threads);

	int rem = points.size() - chunk*threads;
	int offset = 0;

	for (int i=0; i<threads; i++){
		int end = offset + chunk - 1;
		if (rem){
			end++;
			rem--;
		}
		closestK(closest_lists[i], offset, end, p, k);
		// print(closest_lists[i]);
		offset = end+1;
	}

	vector<pair<double, point*> > closest_k;
	find_overall_closest_k(closest_k, k);
	int ans = aggregate(closest_k);
	print(closest_k);
	return ans;
}

int answer_query_parallel(){
	point p;
	for (int i=0; i<dimensions; i++){
		double a;
		cin>>a;
		p.cood.push_back(a);
	}

	int k = K;

	int chunk = points.size()/threads;
	closest_lists.clear();
	closest_lists.resize(threads);

	int rem = points.size() - chunk*threads;
	int offset = 0;

	vector<thread> tds;

	for (int i=0; i<threads; i++){
		int end = offset + chunk - 1;
		if (rem){
			end++;
			rem--;
		}
		tds.push_back(thread(closestK, ref(closest_lists[i]), offset, end, p, k));
		// print(closest_lists[i]);
		offset = end+1;
	}

	for (int i=0; i<threads; i++){
		tds[i].join();
	}

	vector<pair<double, point*> > closest_k;
	find_overall_closest_k(closest_k, k);
	int ans = aggregate(closest_k);
	print(closest_k);
	return ans;
}

int main(){
	read_points();
	int queries;
	cin>>queries;
	while (queries--){
		int lbl = answer_query_parallel();
		cout<<"label: "<<lbl<<endl;
	}
	return 0;
}