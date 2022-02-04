paises = ["EE.UU", "Rusia", "Guatemala", "Alemania"]::Vector{String};
celulares = ["Galaxy A12", "iPhone 13", "Huawei P40"]::Vector{String};
edades = ["12-14", "15-17","18-24","25-30"]::Vector{String};

vendidos = [
    [
        [1800,1600,2000,1500],
        [0,0,0,0],
        [0,0,0,0]
    ],
    [
        [2500,1000,800,4500],
        [0,0,0,0],
        [0,0,0,0]
    ],
    [
        [12500,11000,1800,14500],
        [0,0,0,0],
        [0,0,0,0]
    ],
    [
        [5600,9800,7800,19000],
        [0,0,0,0],
        [0,0,0,0]
    ]
]::Vector{Vector{Vector{Int64}}};


# function insertarValores(array::Vector{Int64})
#     for i in 1:4
#         for j in 2:3
#             array[i][j] = [i+j+3400, i+j+5600, i+j+7600, i+j+2000];
#         end;
#     end;
# end;

function imprimirReporte(value::Int64,i::Int64,j::Int64,k::Int64)
    println(paises[i] * "          " * celulares[j] * "          " * edades[k] * "          " , value);    
end;


function imprimirScore(array::Vector{Int64})
    for i in 1:4
        for j in 1:3
            for k in 1:4
                imprimirReporte(array[i][j][k],i,j,k);
            end;
        end;
    end;
end;



println("Pais" * "          " * "Celular" * "          " * "Edad" * "          " * "Vendidos");    
imprimirScore(vendidos);