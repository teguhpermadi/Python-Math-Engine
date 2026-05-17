import pytest
from app.services.net_service import get_net_supported_shapes, generate_shape_net

def test_get_net_supported_shapes():
    shapes = get_net_supported_shapes()
    assert len(shapes) == 6
    supported_types = {s["type"] for s in shapes}
    expected_types = {"cube", "block", "triangular_prism", "rectangular_pyramid", "cylinder", "cone"}
    assert supported_types == expected_types
    
    # Check that Indonesian names are provided
    for shape in shapes:
        assert "name_id" in shape
        assert isinstance(shape["name_id"], str)
        assert len(shape["name_id"]) > 0

def test_generate_valid_nets():
    supported_shapes = [s["type"] for s in get_net_supported_shapes()]
    
    for shape in supported_shapes:
        # Generate with seed 42 (valid)
        res = generate_shape_net(shape, seed=42, is_valid=True)
        
        assert res["shape"] == shape
        assert res["is_valid"] is True
        assert res["error_reason"] is None
        assert "pattern_name" in res
        assert "grid_size" in res
        assert "faces" in res
        assert len(res["faces"]) > 0
        
        # Verify schema of each face
        for face in res["faces"]:
            assert "id" in face
            assert "shape_type" in face
            assert "label" in face
            assert "x" in face
            assert "y" in face
            assert "color" in face
            
            # shape-specific face properties
            if face["shape_type"] in ("square", "rectangle"):
                assert "width" in face
                assert "height" in face
            elif face["shape_type"] == "circle":
                assert "radius" in face
            elif face["shape_type"] == "sector":
                assert "radius" in face
                assert "angle" in face
                assert "start_angle" in face
            elif face["shape_type"] == "triangle":
                assert "vertices" in face
                assert len(face["vertices"]) == 3
                for pt in face["vertices"]:
                    assert len(pt) == 2

def test_generate_invalid_nets():
    supported_shapes = [s["type"] for s in get_net_supported_shapes()]
    
    for shape in supported_shapes:
        # Generate with seed 100 (invalid)
        res = generate_shape_net(shape, seed=100, is_valid=False)
        
        assert res["shape"] == shape
        assert res["is_valid"] is False
        assert isinstance(res["error_reason"], str)
        assert len(res["error_reason"]) > 0
        assert "pattern_name" in res
        assert "grid_size" in res
        assert "faces" in res
        assert len(res["faces"]) > 0

def test_generate_unsupported_shape():
    with pytest.raises(ValueError):
        generate_shape_net("sphere", seed=42, is_valid=True)

def test_all_cube_and_block_patterns():
    # Verify we can generate all 11 cube patterns
    generated_cube_patterns = set()
    for seed in range(100):
        res = generate_shape_net("cube", seed=seed, is_valid=True)
        assert len(res["faces"]) == 6
        generated_cube_patterns.add(res["pattern_name"])
        
    assert len(generated_cube_patterns) == 11
    
    # Verify we can generate all 4 block patterns
    generated_block_patterns = set()
    for seed in range(100):
        res = generate_shape_net("block", seed=seed, is_valid=True)
        assert len(res["faces"]) == 6
        generated_block_patterns.add(res["pattern_name"])
        
    assert len(generated_block_patterns) == 4

