% 01 knapsack problem
% time is regarded as cost, successful picking rate is regarded as value, total time is regarded as volume of knapsack
% item 1: dove soap; item 2: index card; item 3: bulb;item 4: toy duck; item 5: pen; item 6: highlighter; item 7: outlet-pleg; item 8: expo;item 9: glue
tb = [0 18 36 2 20 38 4 22 40
      18 0 18 20 2 20 22 4 22  
      36 18 0 38 20 2 40 22 4
      2 20 38 0 18 36 2 20 38
      20 2 20 18 0 18 20 2 20
      38 20 2 36 18 0 38 20 2
	  4 22 40 2 20 38 0 18 36
	  22 4 22 20 2 20 18 0 18
	  40 22 4 38 20 2 36 18 0];%time two-dimensional arrays, tb(i,j) means the time to move from bin#i to bin#j
ts = [20 15 15 15 18 20 18 18 15];%time to pick each item
r = [0.33 0.5 0.6 0.4 0.5 0.4 0.5 0.6 0.75];%successful picking rate
n = length(r);%quantity of item
C=300;%assuming the total time is 5 minutes

num = input('number of bin');  %camera input
c = 2*tb(2,num) + ts(num);    %total time to pick item  %original place is bin#2,so tb(2,num) is the time to move

f = zeros(n+1, C+1);
z = zeros(n+1, C+1);

for i = 2:n+1
	for j = 2:C+1
		f(i,j) = f(i-1,j);
        z(i,j) = 0;
		if j > c(i-1)
			if f(i-1,j-c(i-1))+r(i-1) > f(i,j)
			   f(i,j) = f(i-1,j-c(i-1)) + r(i-1);
               z(i,j) = 1;
            end
		end
	end
end
ans = f(n+1, C+1);%solve the 01 knapsack problem and get the value
z;%this array is used to get the number item to be pick

set = [];
i = n+1;
j = C+1;
while i > 1
    if z(i,j) == 1
        set  = [set i-1];
        j = j-c(i-1);
    end
    i = i-1;
end
set;%get the set of item to be pick

seta = sort(set);
s = [];%successful picking rate of items to be pick
for i = 1:n
    if ismember(i,seta) == 1
        s = [s r(i)];
    end
end
%get array s
[o,index] = sort(s,'descend');%sort the array, higher successful picking rate in the front

bin = [];
for i = 1:length(o)
	bin = [bin num(seta(index(i)))]; 
end
bin%decide the picking order--highest successful picking rate first