# needed
import controller as mainController

# main
def main():
	controller = mainController.Controller(True, True)
	controller.Execute()
	return 0

if __name__ == '__main__':
	main()
