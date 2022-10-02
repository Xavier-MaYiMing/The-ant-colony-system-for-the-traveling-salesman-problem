#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 12:47
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : ACS.py
# @Statement : The ant colony system for the traveling salesman problem
# @Reference : Dorigo M, Birattari M, Stutzle T. Ant colony optimization[J]. IEEE computational intelligence magazine, 2006, 1(4): 28-39.
# @Reference : Dorigo M, Gambardella L M.: Ant Colony System: A cooperative learning approach to the Traveling Salesman Problem. IEEE Tr. Evol. Comp. 1, 53-66[J]. 1997, 1(1): 53-66.
import math
import random
import matplotlib.pyplot as plt


def cal_dis(dis, path):
    # calculate the length of the path
    length = 0
    for i in range(len(path) - 1):
        length += dis[path[i]][path[i + 1]]
    return length


def nearest_neighbor_heuristic(distance):
    # Reference: Rosenkrantz D J, Stearns R E, Lewis, II P M. An analysis of several heuristics for the traveling salesman problem[J]. SIAM Journal on Computing, 1977, 6(3): 563-581.
    path = [i for i in range(len(distance))]
    length = 0
    pre_node = random.choice(path)
    first_node = pre_node
    path.remove(pre_node)
    for i in range(len(distance) - 1):
        next_distance = [distance[pre_node][node] for node in path]
        cur_node = path[next_distance.index(min(next_distance))]
        path.remove(cur_node)
        length += distance[pre_node][cur_node]
        pre_node = cur_node
    length += distance[pre_node][first_node]
    return length


def roulette(pooling):
    sum_num = sum(pooling)
    temp_num = random.random()
    probability = 0
    for i in range(len(pooling)):
        probability += pooling[i] / sum_num
        if probability >= temp_num:
            return i
    return len(pooling)


def choose_next_city(dis, tau, beta, q0, ant_path):
    # Choose the next city
    cur_city = ant_path[-1]
    roulette_pooling = []
    unvisited_cities = []
    for city in range(len(dis)):
        if city not in ant_path:
            unvisited_cities.append(city)
            roulette_pooling.append(tau[cur_city][city] * math.pow(1 / dis[cur_city][city], beta))
    if random.random() <= q0:  # exploitation
        index = roulette_pooling.index(max(roulette_pooling))
    else:  # biased exploration
        index = roulette(roulette_pooling)
    return unvisited_cities[index]


def main(coord_x, coord_y, pop, iter, alpha, beta, rho, q0):
    """
    The main function
    :param coord_x: the x coordination
    :param coord_y: the y coordination
    :param pop: the number of ants
    :param iter: the maximum number of iterations
    :param alpha: the pheromone decay parameter
    :param beta: the parameter which determines the relative importance of pheromone versus distance
    :param rho: the parameter for pheromone local updating rule
    :param q0: the probability of exploitation versus exploration
    :return:
    """
    # Step 1. Initialization
    city_num = len(coord_x)  # the number of cities
    dis = [[0 for _ in range(city_num)] for _ in range(city_num)]  # distance matrix
    for i in range(city_num):
        for j in range(i, city_num):
            temp_dis = math.sqrt((coord_x[i] - coord_x[j]) ** 2 + (coord_y[i] - coord_y[j]) ** 2)
            dis[i][j] = temp_dis
            dis[j][i] = temp_dis
    tau0 = 1 / (nearest_neighbor_heuristic(dis) * city_num)
    tau = [[tau0 for _ in range(city_num)] for _ in range(city_num)]  # pheromone matrix
    iter_best = []
    best_path = []
    best_length = 1e6
    start_city = [random.randint(0, city_num - 1) for _ in range(pop)]  # the start city for each ant

    # Step 2. The main loop
    for _ in range(iter):

        # Step 2.1. Construct ant solutions
        ant_path = [[start_city[i]] for i in range(pop)]
        for i in range(city_num):
            if i != city_num - 1:
                for j in range(pop):
                    next_city = choose_next_city(dis, tau, beta, q0, ant_path[j])
                    ant_path[j].append(next_city)
            else:
                for j in range(pop):
                    ant_path[j].append(start_city[j])

            # Step 2.2. Local updating rule
            for j in range(pop):
                pre_city = ant_path[j][-2]
                cur_city = ant_path[j][-1]
                temp_tau = (1 - rho) * tau[pre_city][cur_city] + rho * tau0
                tau[pre_city][cur_city] = temp_tau
                tau[cur_city][pre_city] = temp_tau

        for path in ant_path:
            length = cal_dis(dis, path)
            if length < best_length:
                best_length = length
                best_path = path
        iter_best.append(best_length)

        # Step 2.3. Global updating rule
        for i in range(city_num):
            for j in range(i, city_num):
                tau[i][j] *= (1 - alpha)
                tau[j][i] *= (1 - alpha)
        delta_tau = 1 / best_length
        for i in range(len(best_path) - 1):
            tau[best_path[i]][best_path[i + 1]] += delta_tau
            tau[best_path[i + 1]][best_path[i]] += delta_tau

    # Step 3. Sort the results
    x = [i for i in range(iter)]
    plt.figure()
    plt.plot(x, iter_best, linewidth=2, color='blue')
    plt.title('Convergence curve')
    plt.xlabel('Iterations')
    plt.ylabel('Best so-far value')
    plt.show()

    plt.figure()
    plt.scatter(coord_x, coord_y, color='black')
    for i in range(len(best_path) - 1):
        temp_x = [coord_x[best_path[i]], coord_x[best_path[i + 1]]]
        temp_y = [coord_y[best_path[i]], coord_y[best_path[i + 1]]]
        plt.plot(temp_x, temp_y, color='blue')
    plt.title('The best result')
    plt.xlabel('x coordination')
    plt.ylabel('y coordination')
    plt.show()

    return {'Best tour': best_path, 'Shortest length': best_length}


if __name__ == '__main__':
    # Set the parameters
    pop = 20
    beta = 2
    q0 = 0.9
    alpha = 0.1
    rho = 0.1
    iter = 50
    city_num = 30
    min_coord = 0
    max_coord = 10
    coord_x = [random.uniform(min_coord, max_coord) for _ in range(city_num)]
    coord_y = [random.uniform(min_coord, max_coord) for _ in range(city_num)]
    print(main(coord_x, coord_y, pop, iter, alpha, beta, rho, q0))
