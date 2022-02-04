# Multiplicar impares
function multiplicarImpares(n::Int64)::Int64
    if (n == 0)
        return 0;
    elseif (n == 1)
        return 1;
    else
        if (n % 2 == 0)
            return multiplicarImpares(n - 1);
        else
            return multiplicarImpares(n - 2) * n;
        end;
    end;
end;

println("Multiplicar impares hasta 12: ", multiplicarImpares(12));
println("Multiplicar impares hasta 5: ", multiplicarImpares(5));
println("Multiplicar impares hasta 21: ", multiplicarImpares(21));