
# c++对象模型和this指针

> 成员变量和成员函数分开存储

## this指针
> 指向被调用的成员函数所属的对象
``` 
class Person{
    public:
        int age;
        
        Person(int age){
            this->age = age;
        }
        
        Person& addAge(int age){
            this->age += age;
            return *this;
        }
}

Person p(10);
p.addAge(20).addAge(30);
```

## 空指针访问成员函数
``` 
class Person{
    public:
        int age;
        
        Person(int age){
            this->age = age;
        }
        
        Person& addAge(int age){
        
            if(this == NULL) return ;
            
            this->age += age;
            return *this;
        }
}

```

## const 修饰成员函数
``` 
class Person{
public:

    // 常函数
    // Person* const this                修饰的是this
    // const Person* const this          修饰的是内容
    void showPerson() const{
        // this->a = 100;
    }
    
    int a;
    mutable int b ; // 特殊变量， 即使在常函数也可以修改。
}


// 常对象
const Person p;

```


