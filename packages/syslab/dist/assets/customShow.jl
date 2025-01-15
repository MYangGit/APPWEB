using TyPlot
using TyAntenna
function customShow(
    BoundaryEdges::Union{Vector,AbstractMatrix{Int64}},
    BorderVertices::AbstractMatrix{Float64},
    Polygons::Union{AbstractMatrix{Int64}},
    FeedLocation::Union{Vector{Float64},Matrix{Float64}},
    FeedRadius::Union{Float64,VecOrMat{Float64}},
    name::DataType,
)
    if any(BorderVertices .> 0.9)
        scale = "m"
        r = FeedRadius
    else
        scale = "mm"
        BorderVertices = BorderVertices .* 1000
        FeedLocation = FeedLocation .* 1000
        r = FeedRadius .* 1000
    end
    figure()
    #馈源
    if !isa(FeedRadius, Real)
        r = FeedRadius[1]
    end
    X, Y, Z = sphere(; fig=false)
    X2 = X .* r
    Y2 = Y .* r
    Z2 = Z .* r

    if isa(FeedLocation, Matrix)
        for i in 1:size(FeedLocation, 1)
            feed = surf(
                X2 .+ FeedLocation[i, 1], Y2 .+ FeedLocation[i, 2], Z2 .+ FeedLocation[i, 3]
            )
            feed.set_color("red")
            hold("on")
        end
    else
        for i in 1:size(FeedLocation, 2)
            feed = surf(
                X2 .+ FeedLocation[1, i], Y2 .+ FeedLocation[2, i], Z2 .+ FeedLocation[3, i]
            )
            feed.set_color("red")
            hold("on")
        end
    end
    #坐标轴
    maxx = maximum(BorderVertices[:, 1])
    maxy = maximum(BorderVertices[:, 2])
    maxz = maximum(BorderVertices[:, 3])
    bx = roundup(maxx)
    by = roundup(maxy)
    bz = roundup(maxz)
    pbaspect([bx, by, bz])
    # pbaspect("auto")
    xlim([-bx, bx])
    ylim([-by, by])
    if bz > 40
        zlim([0, 1.1 * bz])
    else
        zlim([-bz, 1.1 * bz])
    end
    if bx == 0
        xticks([])
    elseif (by / bx >= 10) || (by / bx >= 10)
        xticks([])
    elseif (by / bx >= 2) || (maxz / maxx >= 1.5)##cycloid 1.9
        xticks([-bx / 2, 0, bx / 2])
    end
    if by == 0
        yticks([])
    elseif (bx / by >= 10) || (bz / by >= 10)
        yticks([])
    elseif (bx / by >= 1.5) || (bz / by >= 1.5)##cycloid 1.9
        yticks([-by / 2, 0, by / 2])
    end
    if bz == 0
        zticks([])
    elseif (by / bz >= 10) || (bx / bz >= 10)
        zticks([])
    end

    # legend("_none")

    # 面片图

    for i in 1:size(Polygons, 1)
        t = patch(
            BorderVertices[Polygons[i, :], 1],
            BorderVertices[Polygons[i, :], 2],
            BorderVertices[Polygons[i, :], 3],
            "#EDB120",
        )
        # legend("PEC")
        t.set_edgecolor("#EDB120")
        hold("on")
    end

    # 边界图  #用plot，因为与patch一起用边界效果会掩盖，现在图形库不能解决这个问题，后面图形库修复后可用
    # flag = isa(BoundaryEdges, Matrix{Int64})
    # if flag #矩阵
    #     for i in 1:size(BoundaryEdges, 1)
    #         plot3(
    #             BorderVertices[BoundaryEdges[i, :], 1],
    #             BorderVertices[BoundaryEdges[i, :], 2],
    #             BorderVertices[BoundaryEdges[i, :], 3],
    #             "k",
    #         )
    #         hold("on")
    #     end
    # else #矩阵构成的向量
    #     dims = count_nested_vectors(BoundaryEdges)

    #     if dims == 2 || dims == 1
    #         for j in 1:length(BoundaryEdges)
    #             for i in 1:size(BoundaryEdges[j], 1)
    #                 plot3(
    #                     BorderVertices[Int.(BoundaryEdges[j][i, :]), 1],
    #                     BorderVertices[Int.(BoundaryEdges[j][i, :]), 2],
    #                     BorderVertices[Int.(BoundaryEdges[j][i, :]), 3],
    #                     "k",
    #                 )
    #                 hold("on")
    #             end
    #         end
    #     elseif dims == 3
    #         for j in 1:length(BoundaryEdges)
    #             for i in 1:size(BoundaryEdges[j], 1)
    #                 for k in 1:size(BoundaryEdges[j][i], 1)
    #                     aa = BoundaryEdges[j][i][k, :]
    #                     plot3(
    #                         BorderVertices[Int.(BoundaryEdges[j][i][k, :]), 1],
    #                         BorderVertices[Int.(BoundaryEdges[j][i][k, :]), 2],
    #                         BorderVertices[Int.(BoundaryEdges[j][i][k, :]), 3],
    #                         "k",
    #                     )
    #                     hold("on")
    #                 end
    #             end
    #         end
    #     else
    #         error(" ")
    #     end
    # end
    # # 边界图  #用patch，为了解决会掩盖边界线问题的替代方案
    flag = isa(BoundaryEdges, Matrix{Int64})
    if flag #矩阵
        result = [
            [row[i:(i + 1)] for i in 1:(length(row) - 1)] for row in eachrow(BoundaryEdges)
        ]
        pairs0 = vcat(result...)
        BoundaryEdges_new = [vcat(pair, [pair[1]]) for pair in pairs0]

        for i in 1:length(BoundaryEdges_new)
            patch(
                BorderVertices[BoundaryEdges_new[i], 1],
                BorderVertices[BoundaryEdges_new[i], 2],
                BorderVertices[BoundaryEdges_new[i], 3],
                "k",
            )
        end
        hold("on")
    else #矩阵构成的向量
        dims = count_nested_vectors(BoundaryEdges)

        if dims == 2 || dims == 1
            result = [
                [[row[i:(i + 1)] for i in 1:(length(row) - 1)] for row in eachrow(matrix)]
                for matrix in BoundaryEdges
            ]
            pairs0 = vcat(vcat(result...)...)
            BoundaryEdges_new = [vcat(pair, [pair[1]]) for pair in pairs0]

            for i in 1:length(BoundaryEdges_new)
                patch(
                    BorderVertices[BoundaryEdges_new[i], 1],
                    BorderVertices[BoundaryEdges_new[i], 2],
                    BorderVertices[BoundaryEdges_new[i], 3],
                    "k",
                )
                hold("on")
            end
        elseif dims == 3
            result = []
            for matrix in BoundaryEdges
                if isa(matrix, Vector)  # 如果matrix是一个向量，则遍历其中的每个矩阵
                    for submatrix in matrix
                        for row in eachrow(submatrix)
                            for i in 1:(length(row) - 1)
                                push!(result, [row[i], row[i + 1], row[i]])
                            end
                        end
                    end
                else  # 如果matrix是一个矩阵，则直接处理
                    for row in eachrow(matrix)
                        for i in 1:(length(row) - 1)
                            push!(result, [row[i], row[i + 1], row[i]])
                        end
                    end
                end
            end
            BoundaryEdges_new = result
            for i in 1:length(BoundaryEdges_new)
                patch(
                    BorderVertices[BoundaryEdges_new[i], 1],
                    BorderVertices[BoundaryEdges_new[i], 2],
                    BorderVertices[BoundaryEdges_new[i], 3],
                    "k",
                )
            end
        else
            error(" ")
        end
    end
    hold("off")
    title("$(name) antenna element")
    if scale == "mm"
        xlabel("x(mm)")
        ylabel("y(mm)")
        zlabel("z(mm)")
    elseif scale == "m"
        xlabel("x(m)")
        ylabel("y(m)")
        zlabel("z(m)")
    end
    grid("on")
    return nothing
end

function roundup(num)
    if num == 0
        b = 0.1
    elseif num < 1
        decimal = 10^(abs(floor(log10(abs(num)))))
        b = ceil(num * decimal) / decimal
        # bdown = floor(num * decimal) / decimal
    elseif num < 10
        b = ceil(num)
        # bdown = floor(num)
    elseif num < 50
        b = round(num + 5 - num % 5)
    elseif num < 100
        b = round(num + 10 - num % 10)
    elseif num < 150
        b = round(num + 20 - num % 10)
    else
        b = round(num + 100 - num % 100)
    end
    return b
end

function show(obj::cavity)
    name = typeof(obj)
    Geometry = TyAntenna.__Internal__.AntennaCatalog.CavityAntennas.createGeometry(obj)
    BorderVertices = collect(Geometry.BorderVertices)
    if !isa(Geometry.Polygons, Matrix{Int64})
        Polygons = convert(Vector{Matrix{Int64}}, Geometry.Polygons)
        Polygons = vcat(Polygons...)
    end
    BoundaryEdges = Geometry.BoundaryEdges
    if isa(BoundaryEdges, Vector)
        for i in 1:length(BoundaryEdges)
            BoundaryEdges[i] = Int.(hcat(BoundaryEdges[i], BoundaryEdges[i][:, 1]))
        end
    elseif isa(BoundaryEdges, AbstractMatrix)
        BoundaryEdges = Int.(hcat(BoundaryEdges, BoundaryEdges[:, 1]))
    end
    FeedLocation = collect(obj.FeedLocation)
    if isa(obj.Exciter, patchMicrostripEnotch)
        FeedRadius = obj.Exciter.FeedDiameter
    else
        FeedRadius = obj.Exciter.FeedWidth
    end
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end
function show(obj::reflectorCorner)
    # if isa(obj.Exciter, dipole) ||
    #     isa(obj.Exciter, bowtieTriangular) ||
    #     isa(obj.Exciter, bowtieRounded) ||
    #     isa(obj.Exciter, dipoleBlade)
    #     obj.Exciter.Tilt = 90
    #     obj.Exciter.TiltAxis = [0, 1, 0]
    # end
    name = typeof(obj)
    ReflectorGeometry = TyAntenna.__Internal__.AntennaCatalog.ReflectorAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(ReflectorGeometry.BorderVertices)
    Polygons = convert(Vector{Matrix{Int64}}, ReflectorGeometry.Polygons)
    Polygons = vcat(Polygons[1], Polygons[2])
    BoundaryEdges = ReflectorGeometry.BoundaryEdges
    if isa(BoundaryEdges, Vector)
        for i in 1:length(BoundaryEdges)
            BoundaryEdges[i] = Int.(hcat(BoundaryEdges[i], BoundaryEdges[i][:, 1]))
        end
    elseif isa(BoundaryEdges, AbstractMatrix)
        BoundaryEdges = Int.(hcat(BoundaryEdges, BoundaryEdges[:, 1]))
    end
    # BoundaryEdges = ReflectorGeometry.BoundaryEdges
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.FeedWidth / 4
    customShow(BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name)
    return nothing
end
function show(obj::reflectorCircular)
    # if isa(obj.Exciter, dipole) ||
    #     isa(obj.Exciter, bowtieTriangular) ||
    #     isa(obj.Exciter, bowtieRounded) ||
    #     isa(obj.Exciter, dipoleBlade)
    #     obj.Exciter.Tilt = 90
    #     obj.Exciter.TiltAxis = [0, 1, 0]
    # end
    name = typeof(obj)
    ReflectorGeometry = TyAntenna.__Internal__.AntennaCatalog.ReflectorAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(ReflectorGeometry.BorderVertices)
    Polygons = ReflectorGeometry.Polygons
    # if isa(obj.Exciter, dipole)
    if typeof(ReflectorGeometry.Polygons) == Matrix{Float64}
        Polygons = convert(Matrix{Int64}, ReflectorGeometry.Polygons)
    else
        Polygons = convert(Vector{Matrix{Int64}}, ReflectorGeometry.Polygons)
        Polygons = vcat(Polygons[1], Polygons[2])
    end

    BoundaryEdges = ReflectorGeometry.BoundaryEdges
    if isa(ReflectorGeometry.BoundaryEdges, Vector)
        for i in 1:length(ReflectorGeometry.BoundaryEdges)
            BoundaryEdges[i] =
                Int.(
                    hcat(
                        collect(ReflectorGeometry.BoundaryEdges[i]),
                        ReflectorGeometry.BoundaryEdges[i][:, 1],
                    )
                )
        end
    elseif isa(ReflectorGeometry.BoundaryEdges, AbstractMatrix)
        BoundaryEdges =
            Int.(
                hcat(ReflectorGeometry.BoundaryEdges, ReflectorGeometry.BoundaryEdges[:, 1])
            )
    end
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.FeedWidth / 4
    customShow(BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name)
    return nothing
end
function show(obj::reflector)
    # if isa(obj.Exciter, dipole) ||
    #     isa(obj.Exciter, bowtieTriangular) ||
    #     isa(obj.Exciter, bowtieRounded) ||
    #     isa(obj.Exciter, dipoleBlade)
    #     obj.Exciter.Tilt = 90
    #     obj.Exciter.TiltAxis = [0, 1, 0]
    # end
    name = typeof(obj)
    ReflectorGeometry = TyAntenna.__Internal__.AntennaCatalog.ReflectorAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(ReflectorGeometry.BorderVertices)
    Polygons = ReflectorGeometry.Polygons
    # if !isa(obj.Exciter, dipoleVee)
    if !isa(ReflectorGeometry.Polygons, Matrix{Int64})
        Polygons = convert(Vector{Matrix{Int64}}, ReflectorGeometry.Polygons)
        Polygons = vcat(Polygons[1], Polygons[2])
    end
    for i in 1:length(ReflectorGeometry.BoundaryEdges)
        ReflectorGeometry.BoundaryEdges[i] =
            Int.(
                hcat(
                    ReflectorGeometry.BoundaryEdges[i],
                    ReflectorGeometry.BoundaryEdges[i][:, 1],
                )
            )
    end
    BoundaryEdges = ReflectorGeometry.BoundaryEdges
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.FeedWidth / 4
    customShow(BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name)
    return nothing
end

#偶极子天线
function show(obj::bowtieRounded)#12
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices)
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = collect(
        hcat(DipoleGeometry.BoundaryEdges, DipoleGeometry.BoundaryEdges[1])
    )
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.FeedWidth
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::bowtieTriangular)#13
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices)
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = collect(
        hcat(DipoleGeometry.BoundaryEdges, DipoleGeometry.BoundaryEdges[1])
    )
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.FeedWidth
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::biquad)#14
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices)
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = collect(
        hcat(DipoleGeometry.BoundaryEdges, DipoleGeometry.BoundaryEdges[1])
    )
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.FeedWidth
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end
function show(obj::dipole)#15
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices')
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = collect(
        hcat(DipoleGeometry.BoundaryEdges', DipoleGeometry.BoundaryEdges[1])
    )
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.Width / 4
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::dipoleBlade)#16
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices')
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = collect(
        hcat(DipoleGeometry.BoundaryEdges', DipoleGeometry.BoundaryEdges[1])
    )
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.FeedWidth / 4
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::dipoleCrossed)#17
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices')
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = collect(
        hcat(DipoleGeometry.BoundaryEdges', DipoleGeometry.BoundaryEdges[1])
    )
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.FeedWidth / 4
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end
function show(obj::dipoleCycloid)#18
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices)
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = DipoleGeometry.BoundaryEdges
    for i in 1:length(DipoleGeometry.BoundaryEdges)
        DipoleGeometry.BoundaryEdges[i] = collect(
            hcat(DipoleGeometry.BoundaryEdges[i], DipoleGeometry.BoundaryEdges[i][1])
        )
    end
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.FeedWidth
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::dipoleCylindrical)#19
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices)
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = DipoleGeometry.BoundaryEdges
    for i in 1:length(DipoleGeometry.BoundaryEdges)
        DipoleGeometry.BoundaryEdges[i] = collect(
            hcat(DipoleGeometry.BoundaryEdges[i], DipoleGeometry.BoundaryEdges[i][1])
        )
    end
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.FeedWidth
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::dipoleFolded)#20
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices')
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = hcat(DipoleGeometry.BoundaryEdges, DipoleGeometry.BoundaryEdges[:, 1])
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.Width / 4
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::dipoleHelix)#21
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices')
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = hcat(DipoleGeometry.BoundaryEdges, DipoleGeometry.BoundaryEdges[:, 1])
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.Width / 4
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::dipoleHelixMultifilar)#22
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices')
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = Vector{Matrix{Float64}}(undef, length(DipoleGeometry.BoundaryEdges))
    for i in 1:length(DipoleGeometry.BoundaryEdges)
        BoundaryEdges[i] = collect(
            vcat(DipoleGeometry.BoundaryEdges[i], DipoleGeometry.BoundaryEdges[i][1])'
        )
    end
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.Width / 4
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::dipoleJ)#23
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices)
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = DipoleGeometry.BoundaryEdges
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.FeedWidth
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::dipoleMeander)#24
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices)
    Polygons = Int.(DipoleGeometry.Polygons)
    BoundaryEdges = Int.(DipoleGeometry.BoundaryEdges)
    BoundaryEdges = hcat(BoundaryEdges, BoundaryEdges[:, 1])
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.Width / 4
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end
function show(obj::dipoleVee)#25
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices)
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = hcat(DipoleGeometry.BoundaryEdges, DipoleGeometry.BoundaryEdges[:, 1])
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.Width / 4
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::rhombic)#26
    name = typeof(obj)
    DipoleGeometry = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(
        obj
    )
    BorderVertices = collect(DipoleGeometry.BorderVertices)
    Polygons = DipoleGeometry.Polygons
    BoundaryEdges = hcat(DipoleGeometry.BoundaryEdges, DipoleGeometry.BoundaryEdges[:, 1])
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.Width / 4
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::fractalSnowflake)#34
    name = typeof(obj)
    Geometry = TyAntenna.__Internal__.AntennaCatalog.FractalAntennas.createGeometry(obj)
    BorderVertices = collect(Geometry.BorderVertices)
    Polygons = Int.(Geometry.Polygons)
    # BoundaryEdges = hcat(Geometry.BoundaryEdges, Geometry.BoundaryEdges[:, 1])

    for i in 1:length(Geometry.BoundaryEdges)
        Geometry.BoundaryEdges[i] = hcat(
            Geometry.BoundaryEdges[i], Geometry.BoundaryEdges[i][:, 1]
        )
    end

    BoundaryEdges = Geometry.BoundaryEdges
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = obj.GroundPlaneLength / 10
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end
function show(obj::hornConical)#41
    name = typeof(obj)
    Geometry = TyAntenna.__Internal__.AntennaCatalog.HornAntennas.createGeometry(obj)
    BorderVertices = collect(Geometry.BorderVertices)
    Polygons = Int.(collect(Geometry.Polygons))
    # BoundaryEdges = hcat(Geometry.BoundaryEdges, Geometry.BoundaryEdges[:, 1])
    BoundaryEdges = Int.(Geometry.BoundaryEdges)
    FeedLocation = collect(obj.FeedLocation)
    FeedRadius = 0.003
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::rectangularArray)
    FeedLocation = collect(obj.FeedLocation)
    name = typeof(obj)
    Geometry = TyAntenna.__Internal__.AntennaCatalog.Arrays.createGeometry(obj)
    BorderVertices = collect(Geometry.BorderVertices)
    tempPolygons = Geometry.Polygons
    Polygons = Geometry.Polygons

    dims = count_nested_vectors(Polygons)
    if dims == 2
        Polygons = Int.(vcat(Polygons...))
    elseif dims == 3
        Polygons = Int.(vcat(vcat(Polygons...)...))
    end

    BoundaryEdges = collect(Geometry.BoundaryEdges)
    if count_nested_vectors(BoundaryEdges) == 1
        BoundaryEdges = hcat(Int.(BoundaryEdges), Int.(BoundaryEdges[:, 1]))
    elseif count_nested_vectors(BoundaryEdges) == 2
        for i in 1:length(BoundaryEdges)
            BoundaryEdges[i] = hcat(Int.(BoundaryEdges[i]), Int.(BoundaryEdges[i][:, 1]))
        end
    elseif count_nested_vectors(BoundaryEdges) == 3
        for i in 1:length(BoundaryEdges)
            for j in 1:length(BoundaryEdges[i])
                BoundaryEdges[i][j] = hcat(
                    Int.(BoundaryEdges[i][j]), Int.(BoundaryEdges[i][j][:, 1])
                )
            end
        end
    end

    if isa(obj.Element, patchMicrostripEnotch)
        FeedRadius = obj.Element.FeedDiameter
    else
        FeedRadius = obj.Element.FeedWidth / 2
    end
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::linearArray)
    FeedLocation = collect(obj.FeedLocation)
    name = typeof(obj)
    Geometry = TyAntenna.__Internal__.AntennaCatalog.Arrays.createGeometry(obj)
    BorderVertices = collect(Geometry.BorderVertices)
    Polygons = Geometry.Polygons
    dims = count_nested_vectors(Polygons)
    if dims == 2
        Polygons = Int.(vcat(Polygons...))
    elseif dims == 3
        Polygons = Int.(vcat(vcat(Polygons...)...))
    end
    BoundaryEdges = collect(Geometry.BoundaryEdges)
    if count_nested_vectors(BoundaryEdges) == 1
        BoundaryEdges = hcat(Int.(BoundaryEdges), Int.(BoundaryEdges[:, 1]))
    elseif count_nested_vectors(BoundaryEdges) == 2
        for i in 1:length(BoundaryEdges)
            BoundaryEdges[i] = hcat(Int.(BoundaryEdges[i]), Int.(BoundaryEdges[i][:, 1]))
        end
    elseif count_nested_vectors(BoundaryEdges) == 3
        for i in 1:length(BoundaryEdges)
            for j in 1:length(BoundaryEdges[i])
                BoundaryEdges[i][j] = hcat(
                    Int.(BoundaryEdges[i][j]), Int.(BoundaryEdges[i][j][:, 1])
                )
            end
        end
    end

    FeedRadius = obj.Element.FeedWidth / 2
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function show(obj::circularArray)
    FeedLocation = collect(obj.FeedLocation)
    name = typeof(obj)
    Geometry = TyAntenna.__Internal__.AntennaCatalog.Arrays.createGeometry(obj)
    BorderVertices = collect(Geometry.BorderVertices)
    tempPolygons = Geometry.Polygons
    Polygons = Geometry.Polygons

    dims = count_nested_vectors(Polygons)
    if dims == 2
        Polygons = Int.(vcat(Polygons...))
    elseif dims == 3
        Polygons = Int.(vcat(vcat(Polygons...)...))
    end
    BoundaryEdges = collect(Geometry.BoundaryEdges)
    if count_nested_vectors(BoundaryEdges) == 1
        BoundaryEdges = hcat(Int.(BoundaryEdges), Int.(BoundaryEdges[:, 1]))
    elseif count_nested_vectors(BoundaryEdges) == 2
        for i in 1:length(BoundaryEdges)
            BoundaryEdges[i] = hcat(Int.(BoundaryEdges[i]), Int.(BoundaryEdges[i][:, 1]))
        end
    elseif count_nested_vectors(BoundaryEdges) == 3
        for i in 1:length(BoundaryEdges)
            for j in 1:length(BoundaryEdges[i])
                BoundaryEdges[i][j] = hcat(
                    Int.(BoundaryEdges[i][j]), Int.(BoundaryEdges[i][j][:, 1])
                )
            end
        end
    end

    FeedRadius = obj.Element.FeedWidth / 2
    # if occursin(string(name),"reflector")
    #     FeedLocation = collect(obj.FeedLocation)
    #     FeedRadius = obj.Exciter.FeedWidth/2
    # else
    #     FeedLocation = collect(obj.FeedLocation')
    #     FeedRadius = obj.Element.FeedWidth/2
    # end
    return customShow(
        BoundaryEdges, BorderVertices, Polygons, FeedLocation, FeedRadius, name
    )
end

function impedance(antennaObject, freqRange)
    result = TyAntenna.__Internal__.AntennaAnalysis.PortAnalysis.impedance(
        antennaObject, freqRange
    )
    Resistance = real.(result)
    Reactance = imag.(result)
    label = []
    freqmin = minimum(freqRange)
    if 1e2 < freqmin < 1e5
        factor = 1e3
        unit = "kHz"
    elseif 1e5 < freqmin < 1e8
        factor = 1e6
        unit = "MHz"
    elseif 1e8 < freqmin < 1e11
        factor = 1e9
        unit = "GHz"
    elseif 1e11 < freqmin < 1e14
        factor = 1e12
        unit = "THz"
    else
        factor = 1
        unit = "Hz"
    end
    figure()
    if isa(antennaObject, linearArray) ||
        isa(antennaObject, rectangularArray) ||
        isa(antennaObject, circularArray)
        elements_num = size(Resistance, 2)
        for i in 1:elements_num
            plot(freqRange, Resistance[:, i])
            hold("on")
            plot(freqRange, Reactance[:, i])
            label = push!(label, "Resistance" * "$(i)")
            label = push!(label, "Reactance" * "$(i)")
            hold("on")
        end
    else
        plot(freqRange ./ factor, Resistance, freqRange ./ factor, Reactance)
        label = ["Resistance", "Reactance"]
    end
    grid("on")

    xlabel("Frequency($(unit))")
    ylabel("Impedance(ohms)")
    legend(label)

    title("Impedance")
    hold("off")
    return nothing
end

function sparameters(antennaObject, freqRange, refImpedance=50)
    result =
        TyAntenna.__Internal__.AntennaAnalysis.PortAnalysis.sparameters(
            antennaObject, freqRange, refImpedance
        ).Parameters
    if any(result .== Inf)
        error("Inf")
    end
    spa = @. 20 * log10(abs(result))
    freqmin = minimum(freqRange)
    label = []
    if 1e2 < freqmin < 1e5
        factor = 1e3
        unit = "kHz"
    elseif 1e5 < freqmin < 1e8
        factor = 1e6
        unit = "MHz"
    elseif 1e8 < freqmin < 1e11
        factor = 1e9
        unit = "GHz"
    elseif 1e11 < freqmin < 1e14
        factor = 1e12
        unit = "THz"
    else
        factor = 1
        unit = "Hz"
    end
    figure()
    if isa(antennaObject, linearArray) || isa(antennaObject, circularArray)
        for i in 1:(antennaObject.NumElements)
            for j in 1:(antennaObject.NumElements)
                label = push!(label, "db(S" * "$(j)" * "$(i)" * ")")
                plot(freqRange ./ factor, spa[j, i, :])
                hold("on")
            end
        end
    elseif isa(antennaObject, rectangularArray)
        for i in 1:(antennaObject.RowSpacing)
            for j in 1:(antennaObject.ColumnSpacing)
                label = push!(label, "db(S" * "$(j)" * "$(i)" * ")")
                plot(freqRange ./ factor, spa[j, i, :])
                hold("on")
            end
        end
    else
        plot(freqRange ./ factor, spa)
    end
    grid("on")

    xlabel("Frequency($(unit))")
    ylabel("Magnitude (dB)")
    legend(label)
    title("sparameters")
    hold("off")
    return nothing
end

# function rfplot(spa)
#     result =
#         TyAntenna.__Internal__.AntennaAnalysis.PortAnalysis.sparameters(
#             antennaObject, freqRange, refImpedance
#         ).Parameters
#     spa = @. 20 * log10(abs(result))
#     freqmin = minimum(freqRange)
#     if 1e2 < freqmin < 1e5
#         factor = 1e3
#         unit = "kHz"
#     elseif 1e5 < freqmin < 1e8
#         factor = 1e6
#         unit = "MHz"
#     elseif 1e8 < freqmin < 1e11
#         factor = 1e9
#         unit = "GHz"
#     elseif 1e11 < freqmin < 1e14
#         factor = 1e12
#         unit = "THz"
#     else
#         factor = 1
#         unit = "Hz"
#     end
#     figure()
#     plot(freqRange ./ factor, spa)
#     grid("on")
#     xlabel("Frequency($(unit))")
#     ylabel("Impedance(ohms)")
#     return legend(["dB(S11)"])
# end
function count_nested_vectors(arr)
    count = 0
    while isa(arr, VecOrMat)
        count += 1
        arr = arr[1]  # 取出第一个元素继续检查
    end
    return count
end
