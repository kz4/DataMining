import matplotlib.pyplot as plt

# 1) 
# data_x = [4,2,1,2,6,8,7,5]
# data_y = [9,10,2,5,4,4,5,8]
# centroids_x = [2,1,5]
# centroids_y = [10,2,8]
# plt.plot(data_x, data_y, 'bs', label='Data Points')
# plt.plot(centroids_x, centroids_y, 'rD', label='Centroids')
# plt.legend()
# plt.xticks(range(0, 11, 1))
# plt.yticks(range(0, 11, 1))
# plt.title('K Means')
# plt.xlabel('X Axis')
# plt.ylabel('Y Axis')
# plt.grid(True)
# plt.show()

# Centroid Assignment
# alpha_x = [2]
# alpha_y = [10]
# alpha_centroids_x = [2]
# alpha_centroids_y = [10]
# plt.plot(alpha_x, alpha_y, 'rs', label='Data Points')
# plt.plot(alpha_centroids_x, alpha_centroids_y, 'rD', label='Alpha Centroid')
# beta_x = [1, 2]
# beta_y = [2, 5]
# beta_centroids_x = [1]
# beta_centroids_y = [2]
# plt.plot(beta_x, beta_y, 'gs', label='Data Points')
# plt.plot(beta_centroids_x, beta_centroids_y, 'gD', label='Beta Centroid')
# gamma_x = [4, 6, 8, 7, 5]
# gamma_y = [9, 4, 4, 5, 8]
# gamma_centroids_x = [5]
# gamma_centroids_y = [8]
# plt.plot(gamma_x, gamma_y, 'bs', label='Data Points')
# plt.plot(gamma_centroids_x, gamma_centroids_y, 'bD', label='Gamma Centroid')
# plt.legend()
# plt.xticks(range(0, 11, 1))
# plt.yticks(range(0, 11, 1))
# plt.title('K Means')
# plt.xlabel('X Axis')
# plt.ylabel('Y Axis')
# plt.grid(True)
# plt.show()

# 2) 
# data_x = [4,2,1,2,6,8,7,5]
# data_y = [9,10,2,5,4,4,5,8]
# centroids_x = [2,1.5,6]
# centroids_y = [10,3.5,6]
# plt.plot(data_x, data_y, 'bs', label='Data Points')
# plt.plot(centroids_x, centroids_y, 'rD', label='Centroids')
# plt.legend()
# plt.xticks(range(0, 11, 1))
# plt.yticks(range(0, 11, 1))
# plt.title('K Means')
# plt.xlabel('X Axis')
# plt.ylabel('Y Axis')
# plt.grid(True)
# plt.show()

# 3)
# data_x = [4,2,1,2,6,8,7,5]
# data_y = [9,10,2,5,4,4,5,8]
# centroids_x = [3,1.5,6.5]
# centroids_y = [9.5,3.5,5.25]
# plt.plot(data_x, data_y, 'bs', label='Data Points')
# plt.plot(centroids_x, centroids_y, 'rD', label='Centroids')
# plt.legend()
# plt.xticks(range(0, 11, 1))
# plt.yticks(range(0, 11, 1))
# plt.title('K Means')
# plt.xlabel('X Axis')
# plt.ylabel('Y Axis')
# plt.grid(True)
# plt.show()

# 4)
# data_x = [4,2,1,2,6,8,7,5]
# data_y = [9,10,2,5,4,4,5,8]
# centroids_x = [11/3,1.5,7]
# centroids_y = [9,3.5,13/3]
# plt.plot(data_x, data_y, 'bs', label='Data Points')
# plt.plot(centroids_x, centroids_y, 'rD', label='Centroids')
# plt.legend()
# plt.xticks(range(0, 11, 1))
# plt.yticks(range(0, 11, 1))
# plt.title('K Means')
# plt.xlabel('X Axis')
# plt.ylabel('Y Axis')
# plt.grid(True)
# plt.show()

# Final result
alpha_x = [2, 4, 5]
alpha_y = [10, 9, 8]
alpha_centroids_x = [11/3]
alpha_centroids_y = [9]
plt.plot(alpha_x, alpha_y, 'rs', label='Data Points')
plt.plot(alpha_centroids_x, alpha_centroids_y, 'rD', label='Alpha Centroid')
beta_x = [1, 2]
beta_y = [2, 5]
beta_centroids_x = [1.5]
beta_centroids_y = [3.5]
plt.plot(beta_x, beta_y, 'gs', label='Data Points')
plt.plot(beta_centroids_x, beta_centroids_y, 'gD', label='Beta Centroid')
gamma_x = [6, 8, 7]
gamma_y = [4, 4, 5]
gamma_centroids_x = [7]
gamma_centroids_y = [13/3]
plt.plot(gamma_x, gamma_y, 'bs', label='Data Points')
plt.plot(gamma_centroids_x, gamma_centroids_y, 'bD', label='Gamma Centroid')
plt.legend()
plt.xticks(range(0, 11, 1))
plt.yticks(range(0, 11, 1))
plt.title('K Means')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.grid(True)
plt.show()