function design(antennaobj, freq, tune_param=0)
    lambda = 299792458 / freq
    antObjCopy = antennaobj
    if isa(antennaobj, dipole)
        antObjCopy.Length = 0.47 * lambda
        antObjCopy.Width = lambda / 100
    elseif isa(antennaobj, dipoleFolded)
        antObjCopy.Length = 0.465 * (1 + tune_param) * lambda
        antObjCopy.Width = lambda / 200
        antObjCopy.Spacing = lambda / 150
    elseif isa(antennaobj, dipoleBlade)
        antObjCopy.Length = 0.272 * lambda
        antObjCopy.Width = 0.33 * (1 + tune_param) * lambda
        antObjCopy.TaperLength = 0.268 * lambda
        antObjCopy.FeedGap = 0.007 * lambda
        antObjCopy.FeedWidth = 0.007 * lambda
    elseif isa(antennaobj, bowtieTriangular)
        antObjCopy.Length = 0.265 * (1 + tune_param) * lambda
    elseif isa(antennaobj, bowtieRounded)
        antObjCopy.Length = 0.32 * (1 + tune_param) * lambda
    elseif isa(antennaobj, reflector)
        if isa(antObjCopy.Exciter, dipole)
            antObjCopy.Exciter.Length = 0.4403 * lambda
            antObjCopy.Exciter.Width = 0.0147 * lambda
            antObjCopy.Exciter.Tilt = 90
            antObjCopy.Exciter.TiltAxis = "Y"
            antObjCopy.GroundPlaneLength = 0.5871 * lambda
            antObjCopy.GroundPlaneWidth = 0.5871 * lambda
            antObjCopy.Spacing = 0.2202 * lambda
        elseif isa(antObjCopy.Exciter, dipoleCylindrical)
            antObjCopy.Exciter.Length = 0.47 * lambda
            antObjCopy.Exciter.Radius = 0.0093 * lambda
            antObjCopy.Exciter.Tilt = 90
            antObjCopy.Exciter.TiltAxis = 'Y'
            antObjCopy.GroundPlaneLength = 0.5871 * lambda
            antObjCopy.GroundPlaneWidth = 0.5871 * lambda
            antObjCopy.Spacing = 0.3 * lambda
        elseif isa(antObjCopy.Exciter, rhombic)
            tune_param = tunedesign((antObjCopy), antObjCopy.Exciter)
            antObjCopy.Exciter = design(antObjCopy.Exciter, freq, tune_param)
            antObjCopy.Exciter.Tilt = 0
            antObjCopy.Exciter.TiltAxis = 'X'
            antObjCopy.GroundPlaneLength = 2 * lambda
            antObjCopy.GroundPlaneWidth = 2 * lambda
            antObjCopy.Spacing = 0.26 * lambda
        else
            tune_param = tunedesign(antObjCopy, antObjCopy.Exciter)
            antObjCopy.Exciter = design(antObjCopy.Exciter, freq, tune_param)
            d = findMaxLinearDistance(antObjCopy.Exciter)
            L = 0.9 * lambda
            W = 0.9 * lambda
            h = 0.26 * lambda
            if 2 * d > L
                L = 1.01 * 2 * d
            end
            if 2 * d > W
                W = 1.01 * 2 * d
            end
            antObjCopy.GroundPlaneLength = L
            antObjCopy.GroundPlaneWidth = W
            antObjCopy.Spacing = h
            fixBackingStructureSpacing(antObjCopy, freq)
        end
    elseif isa(antennaobj, reflectorCircular)
        if isa(antObjCopy.Exciter, dipole)
            antObjCopy.Exciter.Length = 0.4403 * lambda
            antObjCopy.Exciter.Width = 0.014 * lambda
            antObjCopy.Exciter.Tilt = 90
            antObjCopy.Exciter.TiltAxis = "Y"
            antObjCopy.GroundPlaneRadius = 0.4 * lambda
            antObjCopy.Spacing = 0.2 * lambda
        elseif isa(antObjCopy.Exciter, rhombic)
            tune_param = tunedesign(antObjCopy, antObjCopy.Exciter)
            antObjCopy.Exciter = design(antObjCopy.Exciter, freq, tune_param)
            antObjCopy.Exciter.Tilt = 0
            antObjCopy.Exciter.TiltAxis = "X"
            antObjCopy.GroundPlaneRadius = 1.2 * lambda / 2
            antObjCopy.Spacing = 0.26 * lambda
        elseif isa(antObjCopy.Exciter, dipoleCylindrical)
            antObjCopy.Exciter.Length = 0.47 * lambda
            antObjCopy.Exciter.Radius = lambda / 107
            antObjCopy.Exciter.Tilt = 90
            antObjCopy.Exciter.TiltAxis = "Y"
            antObjCopy.GroundPlaneRadius = 0.4 * lambda
            antObjCopy.Spacing = 0.3 * lambda
        else
            tune_param = tunedesign(antObjCopy, antObjCopy.Exciter)
            antObjCopy.Exciter = design(antObjCopy.Exciter, freq, tune_param)
            d = findMaxLinearDistance(antObjCopy.Exciter)
            h = 0.26 * lambda
            R = 0.9 * lambda / 2
            if d > R
                R = 1.01 * d
            end
            antObjCopy.GroundPlaneRadius = R
            antObjCopy.Spacing = h
            fixBackingStructureSpacing(antObjCopy, freq)
        end
    elseif isa(antennaobj, reflectorCorner)
        if isa(antObjCopy.Exciter, dipole)
            antObjCopy.Exciter.Length = 0.4403 * lambda
            antObjCopy.Exciter.Width = 0.0147 * lambda
            antObjCopy.Exciter.Tilt = 90
            antObjCopy.Exciter.TiltAxis = "Y"
            antObjCopy.GroundPlaneLength = 0.5871 * lambda
            antObjCopy.GroundPlaneWidth = 2 * 0.5871 * lambda
            antObjCopy.Spacing = 0.2202 * lambda
        elseif isa(antObjCopy.Exciter, dipoleCylindrical)
            antObjCopy.Exciter.Length = 0.44 * lambda
            antObjCopy.Exciter.Radius = 0.009 * lambda
            antObjCopy.Exciter.Tilt = 90
            antObjCopy.Exciter.TiltAxis = "Y"
            antObjCopy.GroundPlaneLength = 0.5871 * lambda
            antObjCopy.GroundPlaneWidth = 2 * 0.5871 * lambda
            antObjCopy.Spacing = 0.5 * lambda
        elseif isa(antObjCopy.Exciter, rhombic)
            tune_param = tunedesign(antObjCopy, antObjCopy.Exciter)
            antObjCopy.Exciter = design(antObjCopy.Exciter, freq, tune_param)
            antObjCopy.Exciter.Tilt = 0
            antObjCopy.Exciter.TiltAxis = "X"
            antObjCopy.GroundPlaneLength = 1.8 * lambda
            antObjCopy.GroundPlaneWidth = 1.8 * lambda
            antObjCopy.Spacing = 0.26 * lambda
            antObjCopy.CornerAngle = 140
        else
            tune_param = tunedesign(antObjCopy, antObjCopy.Exciter)
            antObjCopy.Exciter = design(antObjCopy.Exciter, freq, tune_param)
            d = findMaxLinearDistance(antObjCopy.Exciter)
            L = 0.9 * lambda
            W = 0.9 * lambda
            h = 0.34 * lambda
            if 2 * d > L
                L = 1.05 * 2 * d
            end
            if 2 * d > W
                W = 1.05 * 2 * d
            end
            antObjCopy.GroundPlaneLength = L
            antObjCopy.GroundPlaneWidth = W
            antObjCopy.CornerAngle = 140
            antObjCopy.Spacing = h
            fixBackingStructureSpacing(antObjCopy, freq)
        end
    end
    designObj = antObjCopy
    return designObj
end

function tunedesign(BackingStructure, Exciter)
    tune_param = 0
    check = ["reflector", "reflectorCircular", "reflectorCorner"]
    backingtype = isequal.("$(BackingStructure)", check)
    if isa(Exciter, dipoleBlade)
        if backingtype[1] || backingtype[2]
            tune_param = 0.03
        end
    elseif isa(Exciter, dipole)
    elseif isa(Exciter, dipoleFolded)
        if backingtype[1] == 1
            tune_param = -0.03
        elseif backingtype[2] == 1
            tune_param = -0.035
        elseif backingtype[3] == 1
            tune_param = -0.015
        end
    elseif isa(Exciter, dipoleVee)
    elseif isa(Exciter, dipoleMeander)
        if backingtype[1] || backingtype[2]
            tune_param = -0.03
        end
    elseif isa(Exciter, bowtieTriangular)
    elseif isa(Exciter, bowtieRounded)
    elseif isa(Exciter, dipoleCycloid)
    elseif isa(Exciter, dipoleJ)
    end
    return tune_param
end

using TyMath
function findMaxLinearDistance(elem)
    geom = TyAntenna.__Internal__.AntennaCatalog.DipoleAntennas.createGeometry(elem)
    if isa(elem, dipoleBlade) || isa(elem, dipoleFolded)
        geom.BorderVertices = collect(geom.BorderVertices')
    end
    _, dist = dsearchn([0 0 0], collect(geom.BorderVertices))
    d = maximum(dist)
    return d
end

using TyBase
function fixBackingStructureSpacing(obj, freq)
    ftest = freq / 10
    if ftest < 1e3
        ftest = 1e3
    end
    lambda_test = 299792458 / ftest
    flag = true
    mesherror = []
    # if hasfield(typeof(obj), :Substrate)&& !isa(obj,reflectorCorner)
    #     d = obj.Substrate
    #     dtest = dielectric()
    #     obj.Substrate = dtest
    # end
    nominalSpacing = obj.Spacing
    numChks = 2
    chkIndx = 1
    while flag
        try
            chkIndx = chkIndx + 1
            if isempty(mesherror) && (chkIndx > numChks)
                flag = false
            end
            if chkIndx <= numChks
                obj.Spacing = 1.1 * nominalSpacing
            end
        catch
            nominalSpacing = 1.1 * nominalSpacing
            obj.Spacing = nominalSpacing
            mesherror = []
        end
    end

    # if hasfield(typeof(obj), :Substrate)
    #     obj.Substrate = d
    # end
end
