# ========================== SE MODIFICARON LOS TIPOS =========================
random = [1.0, 5.0, 8.0, -1.0, 21.0, 42.0, -55.0, 123.0, -5.0, 5.0, 11.0]::Vector{Float64};

a = [
    [
        (random[1] * 3) / 1.0,
        51.0,
        random[4] / 2,
        (random[3] * 10) % 7
    ], 
    [
        1.0,
        2.0,
        3.0,
        4.0
    ]
]::Vector{Vector{Float64}};

b = [
    [
        1.0,
        2.0,
        3.0,
        4.0 
    ], 
    [
        (random[1] * 3) / 1,
        51.0,
        random[4] / 2,
        (random[3] * 10) % 7
    ]
]::Vector{Vector{Float64}};

auxiliar = [
    [
        0.0,
        0.0,
        0.0,
        0.0
    ], 
    [
        0.0,
        0.0,
        0.0,
        0.0
    ]
]::Vector{Vector{Float64}};

auxiliar = [
    [
        0.0,
        0.0,
        0.0,
        0.0
    ], 
    [
        0.0,
        0.0,
        0.0,
        0.0
    ]
]::Vector{Vector{Float64}};



# Se cambio la forma en que se recorre el arreglo :v

function printMatriz(matrix::Vector{Vector{Float64}})
    println("[");
    for i in 1:2
        print("[");
        for j in 1:4
            print(matrix[i][j], " ");
        end;
        println("]");
    end;
    println("]");
end;

println("MATRIZ a");
printMatriz(a);

println("");
println("MATRIZ b");
printMatriz(b);



# Se le cambio el retorno y la forma en que recorre 
function sumarMatrices(matrix1::Vector{Vector{Float64}}, matrix2::Vector{Vector{Float64}})::Int64
    # if length(matrix1) != length(matrix2)
    #     println("NO SE PUEDEN SUMAR. NO SON DE LA MISMA LONGITUD")
    #     return 0;
    # end;
    for i in 1:2
        for j in 1:4
            auxiliar[i][j] = matrix1[i][j] + matrix2[i][j];
        end;
    end;
    return 0;
end;


println("");
println("LAS DOS MATRICES SUMADAS");
println(sumarMatrices(a, b));
printMatriz(auxiliar);



# Se le cambio el retorno y la forma en que recorre 
function compararMatrices(matrix1::Vector{Vector{Float64}}, matrix2::Vector{Vector{Float64}})::Bool
    # if length(matrix1) != length(matrix2)
    #     return false;
    # end;

    
    for i in 1:2
        for j in 1:4
            if matrix1[i][j] != matrix2[i][j]
                return false;
            end;
        end;
    end;
    return true;
end;

println();
println("COMPARAR MATRICES. SON IGUALES?");
println(compararMatrices(a, b));

println("")



# b = a;
# println();
# println("COMPARAR MATRICES. SON IGUALES?");
# println(compararMatrices(a, b));