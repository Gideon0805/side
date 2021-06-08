import numpy as np

def main():
	A1 = np.random.rand(4096,1024)*0.001
	B1 = np.random.rand(1024,512)*0.01
	B2 = np.random.rand(512,256)
	B3 = np.random.rand(256,2)

	A2 = np.matmul(A1, B1)
	A3 = np.matmul(A2, B2)
	C = np.matmul(A3, B3)

	np.savetxt('FloatInputA1.txt', A1, fmt='%10.7f', delimiter='\n')
	np.savetxt('FloatInputB1.txt', B1, fmt='%10.7f', delimiter='\n')
	np.savetxt('FloatInputB2.txt', B2, fmt='%10.7f', delimiter='\n')
	np.savetxt('FloatInputB3.txt', B3, fmt='%10.7f', delimiter='\n')
	np.savetxt('FloatOutputC.txt', C, fmt='%10.7f', delimiter='\n')

if __name__ == '__main__':
	main()