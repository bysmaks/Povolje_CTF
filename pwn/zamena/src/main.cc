#include <string>
#include <iostream>

void menu() {
  std::cout<<"Enter 1 to change your string"<<"\n";
  std::cout<<"Enter 2 to exit"<<"\n";
}

int get_int() {
  int retval = 0;
  while(true) {
    std::cin>>retval;
    if(std::cin.fail()){
      continue;
    }
    break;
  }
  return retval;
}

int main() {
  std::string name;
  std::cout<<"Enter your name"<<"\n";
  std::cin>>name;
  int option = 0;
  int idx = 0;
  char babir;
  while(true){
    menu();
    option = get_int();
    switch(option) {
      case 1:
        std::cout<<"Enter index to replace"<<"\n";
        idx = get_int();
        std::cout<<"Enter char to replace"<<"\n";
        std::cin>>babir;
        name[idx] = babir;
        std::cout<<"New string: "<<name<<"\n";
      break;
      case 2:
        return 0;
      break;
      default:
        std::cout<<"Invalid option"<<"\n";
      break;
    }

  }
}
