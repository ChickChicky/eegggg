# EEGGGG
----

## EGG but more... EGG ?

This is a kind of stupid stack-based programming language I made cuz I thought it would be fun ¯\_(ツ)_/¯.



# How to write programs
----

To push values on top of the stack, simply write them down ! (it can only process floats and strings)
```
10
```
The program above pushes the number `10` on top of the stack - and that's it !

<br>

To display what's on the stack, use `@`:
```
42 @
```
>	42

<br>

To invert the last two values on top of the stack, use `~#`:
```
1 2 ~# @
```
>	2	1

Currently, all `#` instructions have a `:` variant which takes one more parameter, the size.<br>
`~:` pops the stack and reverses the *n* last items of it:
```
1 2 3 4 5
3 ~:
@
```
>	1	2	5	4	3

<br>

You can clone the last value on the stack by using `#`:
```
"hello" # @
```
>	hello	hello

This one also has a `:` variant, but also the last variant for these, `::`, which basically does the same thing as `:` but in reverse, well, most of the time, because here, it just allows to repeat the process several times:
```
1 2 
2 :
@
```
>	1	2	1	2
```
1 2
2 3 ::
@
```
>	1	2	1	2	1	2

<br>

You can clear the stack using `;`:
```
1 2 3 @ ;
4 5 6 @
```
>	1	2	3 <br>
>	4	5	6

<br>

I almost forgot MATH !<br>
For your most favourite math operations (*+ - \* / % \*\**), just write them down ! It will pop two values from the stack, and push back the result:
```
8 2 / @
```
>	4

There also are the classic comparison operators (*< > == >= <=*), they pop two values from the stack and puh back the result of the comparison:
```
2 3 < @ ;
2 3 > @ ;
6 6 == @
```
>	1 <br>
>	0 <br>
>	1

<br>

Let's take a look at functions ! To declare one, simply start with `f` and then the name of your function. To close it, simply use `end`:
```
f soom 
    2 : +
end
```

Now, we can start using it, to do so, simply write its name:
```
f soom 2 : + end

3 5 soom @
```
>	3	5	8

The function *soom* copies the last two values on top of the stack and sums them up

<br>

LABELS ! They allow to have some sort of control flow. <br>
BEWARE ! Labels are bound to the context they are created in although they're available everywhere. This means that a label inside of a function only makes sense in that function and will not work as expected if you use it outside of that function.

Let's look at unconditionnal jumps, they are done with `!`, which pops the stack and jumps to the retrieved addresss:
```
forever: ;
    "AAAAA" @
forever !
```
>	AAAAA <br>
>	AAAAA <br>
>	... (forever)

But do you know what's even cooler ? CONDITIONNAL JUMPS ! The `?` instruction pops the stack twice, the first one is the condition, if this value is above 0, the program jumps to the second popped address, if not, then it continues:
```
3 2 >
yes ?
no !

yes:
    "comparison succeeded" @
    anyway !
no:
    "comparison failed" @
    anyway !
anyway:
```
>	comparison succeeded

<br>

I actually kinda lied when I said that the language was stack-based, it actually is **STACK-STACK-BASED** ! <br>
Yeah, instead of relying on one single poor stack, there is a stack of stacks ! By default, the program starts with just one stack, but you can create more ! <br>
By the way, everything before this still works, but when I refer to the term *stack* (when I am not referring to the global concept of stacks, nor I am referring to the *stacks stack*), I refer to the last stack on the stacks stacck.

To push a new stack on the stacks stack, use `{` and to pop one `}`:
```
1 2 3 @
{
    "wut ?" @
}
@
```
>	1	2	3 <br>
>	wut <br>
>	1	2	3

<br>

Of course this would be a bit uninteresting if you couldn't move data between stacks...<br>
For these, there are prefixes and suffixes, which are `>` and `<` and then `#`, `:` and `::`.

`>` indicates that it will pop from the second-to-last stack on the stacks stack and push to the last stack on the stacks stack. <br>
`<` indicates that it will pop from the last stack on the stacks stack and push to the second-to-last stack on the stacks stack. <br>

`#` indicates that a single value is going to be moved. <br>
`:` indicates that *n* values are going to be moved, the stack is popped and the retrieved value becomes *n*. <br>
`::` does the same as `:` but also reverses the pushed values. <br>

A few examples of how this works:
```
"hi"
{
    @
}
@
{
    >#
    @
}
@
```
>	 <br>
>	hi <br>
>	hi <br>
>	<br>
```
f pop
    { ># >: }
end

1 2 3 4 5
@

1 pop
@

3 pop
@
```
>	1	2	3	4	5 <br>
>	1	2	3	4 <br>
>	1 <br>
```
f pop_until
    pu_loop:
        2 : ==
        pu_eq ?
        ~# { ># }
        pu_loop !
    pu_eq:
        { ># }
end

1 2 3 4 5 @
2 pop_until @
```
>	1	2	3	4	5 <br>
>	1	2