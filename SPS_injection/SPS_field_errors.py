def assign_MBA_errors_26GeV(madx, random=True, seed=98634628):
    madx.input("b3a=-2.8e-3;")
    madx.input("b5a=-7.9e+0;")
    madx.input("b7a=+8.8e+4;")
    if random:
        madx.input("b3ar=b3a*0.25;")
        madx.input("b5ar=b5a*0.25;")
        madx.input("b7ar=b7a*0.25;")

    madx.input(f"eoption, seed={seed};")
    madx.input("select, flag=error, clear=true;")
    madx.input("select, flag=error, class=multipole, pattern=\"^MBA\";")
    madx.input("efcomp, dkn:={0., 0., b3a + b3ar*tgauss(3), 0., b5a + b5ar*tgauss(3), 0., b7a + b7ar*tgauss(3)};")
    return

def assign_MBB_errors_26GeV(madx, random=True, seed=98634628):
    madx.input("b3b=+1.6e-3;")
    madx.input("b5b=-6.8e+0;")
    madx.input("b7b=+1.7e+5;")
    if random:
        madx.input("b3br=b3b*0.25;")
        madx.input("b5br=b5b*0.25;")
        madx.input("b7br=b7b*0.25;")

    madx.input(f"eoption, seed={seed};")
    madx.input("select, flag=error, clear=true;")
    madx.input("select, flag=error, class=multipole, pattern=\"^MBB\";")
    madx.input("efcomp, dkn:={0., 0., b3b + b3br*tgauss(3), 0., b5b + b5br*tgauss(3), 0., b7b + b7br*tgauss(3)};")
    return
