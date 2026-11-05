example_set2={True,1,1,0,0,True,False}
print(example_set2)



def outer_func():
    def inner_func():
        print("Hello, World!")
    inner_func()
outer_func()