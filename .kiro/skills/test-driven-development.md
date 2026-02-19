# Test-Driven Development (TDD) Skill

## When to Activate
Use this skill when:
- Writing new features that require tests
- Fixing bugs (always write test first)
- Refactoring existing code
- User explicitly requests TDD approach

## TDD Workflow

### Red-Green-Refactor Cycle

1. **RED: Write a Failing Test**
   - Write the smallest test that fails
   - Test should define the desired behavior
   - Run test to confirm it fails (for the right reason)

2. **GREEN: Make It Pass**
   - Write minimal code to make the test pass
   - Don't worry about perfection yet
   - Focus on making the test green

3. **REFACTOR: Improve the Code**
   - Clean up the code while keeping tests green
   - Remove duplication
   - Improve naming and structure
   - Run tests frequently during refactoring

### Example TDD Session

#### Step 1: Write Failing Test
```python
# test_models.py
def test_block_calculate_total_mass_with_components():
    """Test that total mass calculation includes all components"""
    ore = Ore.objects.create(name="Iron", mass=1.0)
    component = Component.objects.create(
        name="Steel Plate",
        mass=2.0,
        materials={str(ore.id): 3}
    )
    block = Block.objects.create(
        name="Light Armor",
        mass=5.0,
        components={str(component.id): 10}
    )
    
    # This will fail because method doesn't exist yet
    total_mass = block.calculate_total_mass()
    
    expected_mass = 5.0 + (2.0 * 10)  # block mass + component mass * quantity
    assert total_mass == expected_mass
```

#### Step 2: Make It Pass
```python
# models.py
class Block(models.Model):
    name = models.CharField(max_length=100)
    mass = models.FloatField()
    components = models.JSONField(default=dict)
    
    def calculate_total_mass(self):
        """Calculate total mass including components"""
        total = self.mass
        for component_id, quantity in self.components.items():
            component = Component.objects.get(id=component_id)
            total += component.mass * quantity
        return total
```

#### Step 3: Refactor
```python
# models.py
class Block(models.Model):
    name = models.CharField(max_length=100)
    mass = models.FloatField()
    components = models.JSONField(default=dict)
    
    def calculate_total_mass(self) -> float:
        """
        Calculate total mass including all components.
        
        Returns:
            float: Total mass of block plus all components
        """
        component_mass = sum(
            Component.objects.get(id=comp_id).mass * quantity
            for comp_id, quantity in self.components.items()
        )
        return self.mass + component_mass
```

## TDD for Bug Fixes

### Bug Fix Workflow

1. **Reproduce the Bug**
   - Write a test that demonstrates the bug
   - Test should fail, confirming the bug exists

2. **Fix the Bug**
   - Modify code to make the test pass
   - Ensure fix doesn't break other tests

3. **Verify the Fix**
   - Run all tests to ensure no regressions
   - Consider edge cases and add more tests

### Example Bug Fix

```python
# Bug Report: BuildOrder crashes when quantity is zero

# Step 1: Write test that reproduces bug
def test_build_order_with_zero_quantity_raises_error():
    """Test that zero quantity raises ValidationError"""
    block = Block.objects.create(name="Test Block")
    
    with pytest.raises(ValidationError):
        BuildOrder.objects.create(
            name="Test Order",
            blocks={str(block.id): 0}  # Zero quantity should be invalid
        )

# Step 2: Fix the bug
class BuildOrder(models.Model):
    name = models.CharField(max_length=100)
    blocks = models.JSONField(default=dict)
    
    def clean(self):
        """Validate that all quantities are positive"""
        for block_id, quantity in self.blocks.items():
            if quantity <= 0:
                raise ValidationError(
                    f"Quantity must be positive, got {quantity}"
                )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# Step 3: Add edge case tests
def test_build_order_with_negative_quantity_raises_error():
    """Test that negative quantity raises ValidationError"""
    block = Block.objects.create(name="Test Block")
    
    with pytest.raises(ValidationError):
        BuildOrder.objects.create(
            name="Test Order",
            blocks={str(block.id): -5}
        )
```

## TDD Best Practices

### Test Naming
- Use descriptive names: `test_<what>_<condition>_<expected>`
- Examples:
  - `test_create_block_with_valid_data_succeeds`
  - `test_calculate_mass_with_zero_components_returns_base_mass`
  - `test_delete_ore_with_dependencies_prevents_deletion`

### Test Structure (Arrange-Act-Assert)
```python
def test_example():
    # Arrange: Set up test data
    ore = Ore.objects.create(name="Iron", mass=1.0)
    
    # Act: Perform the action
    result = ore.calculate_something()
    
    # Assert: Verify the result
    assert result == expected_value
```

### Keep Tests Independent
```python
# BAD: Tests depend on each other
def test_create_ore():
    ore = Ore.objects.create(name="Iron")
    return ore  # Don't do this

def test_ore_mass(test_create_ore):
    ore = test_create_ore  # Depends on previous test
    assert ore.mass > 0

# GOOD: Each test is independent
@pytest.fixture
def iron_ore():
    return Ore.objects.create(name="Iron", mass=1.0)

def test_create_ore():
    ore = Ore.objects.create(name="Iron")
    assert ore.name == "Iron"

def test_ore_mass(iron_ore):
    assert iron_ore.mass == 1.0
```

### Test One Thing at a Time
```python
# BAD: Testing multiple things
def test_block_operations():
    block = Block.objects.create(name="Test")
    assert block.name == "Test"
    assert block.calculate_mass() > 0
    assert block.validate_components()
    # Too many assertions

# GOOD: Separate tests
def test_block_creation_sets_name():
    block = Block.objects.create(name="Test")
    assert block.name == "Test"

def test_block_calculate_mass_returns_positive():
    block = Block.objects.create(name="Test", mass=10.0)
    assert block.calculate_mass() > 0

def test_block_validate_components_with_valid_data():
    block = Block.objects.create(name="Test")
    assert block.validate_components() is True
```

## TDD Anti-Patterns to Avoid

### Don't Write Tests After Code
- Defeats the purpose of TDD
- Tests may be biased by implementation
- Miss edge cases

### Don't Skip the Refactor Step
- Code quality degrades over time
- Technical debt accumulates
- Tests become harder to maintain

### Don't Write Too Much Code at Once
- Write minimal code to pass test
- Add complexity incrementally
- Keep feedback loop tight

### Don't Test Implementation Details
```python
# BAD: Testing internal implementation
def test_block_uses_specific_algorithm():
    block = Block.objects.create(name="Test")
    assert block._internal_calculation_method() == "specific_algorithm"

# GOOD: Testing behavior
def test_block_calculates_correct_mass():
    block = Block.objects.create(name="Test", mass=10.0)
    assert block.calculate_mass() == 10.0
```

## TDD with Django

### Model Testing
```python
def test_ore_str_representation():
    ore = Ore.objects.create(name="Iron Ore")
    assert str(ore) == "Iron Ore"

def test_ore_mass_must_be_positive():
    with pytest.raises(ValidationError):
        ore = Ore(name="Iron", mass=-1.0)
        ore.full_clean()
```

### View Testing
```python
def test_block_list_view_returns_all_blocks(client):
    Block.objects.create(name="Block 1")
    Block.objects.create(name="Block 2")
    
    response = client.get('/blocks/')
    
    assert response.status_code == 200
    assert len(response.context['object_list']) == 2

def test_block_create_view_with_valid_data(client):
    data = {'name': 'New Block', 'mass': 10.0}
    response = client.post('/blocks/create/', data)
    
    assert response.status_code == 302  # Redirect after success
    assert Block.objects.filter(name='New Block').exists()
```

### Form Testing
```python
def test_block_form_with_valid_data():
    form_data = {'name': 'Test Block', 'mass': 10.0}
    form = BlockForm(data=form_data)
    
    assert form.is_valid()

def test_block_form_with_invalid_mass():
    form_data = {'name': 'Test Block', 'mass': -10.0}
    form = BlockForm(data=form_data)
    
    assert not form.is_valid()
    assert 'mass' in form.errors
```

## Measuring TDD Success

### Code Coverage
- Aim for >80% coverage
- 100% coverage doesn't guarantee quality
- Focus on meaningful tests

### Test Quality Indicators
- Tests are easy to read and understand
- Tests run fast (<1s for unit tests)
- Tests are independent
- Tests catch bugs before production
- Refactoring is safe with good test coverage

### Red-Green-Refactor Metrics
- Time in red: Should be short (minutes)
- Time in green: Should be short (minutes)
- Refactor frequency: After every green cycle
- Test-to-code ratio: Varies, but typically 1:1 to 2:1

## TDD Checklist

Before writing code:
- [ ] Write a failing test first
- [ ] Test fails for the right reason
- [ ] Test is minimal and focused

While writing code:
- [ ] Write minimal code to pass test
- [ ] Run tests frequently
- [ ] Keep feedback loop tight

After test passes:
- [ ] Refactor code for clarity
- [ ] Remove duplication
- [ ] Improve naming
- [ ] All tests still pass

Before committing:
- [ ] All tests pass
- [ ] Code is clean and readable
- [ ] Coverage is maintained/improved
- [ ] No commented-out code
