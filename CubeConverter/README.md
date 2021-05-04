# Cube Converter - Blender Add-on

It's a cubic converter for a specific case, the 3D printer.



## Why

When I'm trying to print a cube-based structure for my puzzle collection,  the material will extend a little and it can't fit.

So I'm trying to find a better way, for efficiently generating such structure as well as solving the unfit problem.

![pic](pic\pic.png)

## How to use

### install

This is a standard Blender Add-On, supporting blender later than 2.80.

About how to install it, you can refer to the official manual.

https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html



### .cube file

This is a type I defined for cube structure input.

Separator is '#', \n', '\t' & ','



Example,

> 1,1,0	0,0,0	0,0,0
> 1,0,0	0,0,0	0,0,0
> 1,1,0	0,1,0	0,1,1
> #<== separate two block
> 1,0,0	1,0,0	0,0,0
> 0,0,0	1,0,0	0,0,0
> 1,1,0	1,0,0	1,0,0



That's the result for the above .cube.

![cubefile](pic\cubefile.png)

## Result

The result within the Blender.

![STLresult](pic\STLresult.png)

Actual printed-out result.

![resultcube](pic\resultcube.png)

## Note

I'm not an expert with 3D print, but I found for the following case, the hinge is much easier to remove in fig b than fig a. You may want to use this property to optimize the layout.

![hinge](pic\hinge.png)

## Further

- Interactive .cube file generation

- Fix the hole

![limit](pic\limit.png)