# Refactoring Patterns Skill

## When to Activate
Use this skill when:
- Code smells are detected
- Improving code maintainability
- Preparing for new features
- Reducing technical debt
- Code review suggests improvements

## Refactoring Principles

### Golden Rules
1. **Always have tests first** - Refactoring without tests is rewriting
2. **Make small changes** - One refactoring at a time
3. **Run tests frequently** - After each small change
4. **Commit often** - Easy to revert if something breaks
5. **Don't change behavior** - Refactoring changes structure, not functionality

### When to Refactor
- Before adding new features (make room)
- During code review (improve quality)
- When you touch old code (boy scout rule)
- When tests are hard to write (design issue)
- When code is hard to understand (clarity issue)

### When NOT to Refactor
- When tests don't exist (write tests first)
- When deadline is critical (technical debt is okay temporarily)
- When rewrite is better (sometimes starting fresh is faster)
- When you don't understand the code (learn it first)

## Common Code Smells

### Long Method
**Smell**: Method is too long (>20 lines)
**Fix**: Extract smaller methods

```python
# BEFORE: Long method
def process_build_order(build_order):
    # Validate input
    if not build_order.blocks:
        raise ValueError("No blocks")
    for block_id, qty in build_order.blocks.items():
        if qty <= 0:
            raise ValueError("Invalid quantity")
    
    # Calculate resources
    total_components = {}
    for block_id, qty in build_order.blocks.items():
        block = Block.objects.get(id=block_id)
        for comp_id, comp_qty in block.components.items():
            total_components[comp_id] = total_components.get(comp_id, 0) + comp_qty * qty
    
    # Calculate ores
    total_ores = {}
    for comp_id, comp_qty in total_components.items():
        component = Component.objects.get(id=comp_id)
        for ore_id, ore_qty in component.materials.items():
            total_ores[ore_id] = total_ores.get(ore_id, 0) + ore_qty * comp_qty
    
    return total_ores

# AFTER: Extracted methods
def process_build_order(build_order):
    validate_build_order(build_order)
    components = calculate_required_components(build_order)
    ores = calculate_required_ores(components)
    return ores

def validate_build_order(build_order):
    if not build_order.blocks:
        raise ValueError("No blocks")
    for block_id, qty in build_order.blocks.items():
        if qty <= 0:
            raise ValueError("Invalid quantity")

def calculate_required_components(build_order):
    total_components = {}
    for block_id, qty in build_order.blocks.items():
        block = Block.objects.get(id=block_id)
        for comp_id, comp_qty in block.components.items():
            total_components[comp_id] = total_components.get(comp_id, 0) + comp_qty * qty
    return total_components

def calculate_required_ores(components):
    total_ores = {}
    for comp_id, comp_qty in components.items():
        component = Component.objects.get(id=comp_id)
        for ore_id, ore_qty in component.materials.items():
            total_ores[ore_id] = total_ores.get(ore_id, 0) + ore_qty * comp_qty
    return total_ores
```

### Duplicate Code
**Smell**: Same code appears in multiple places
**Fix**: Extract to shared function

```python
# BEFORE: Duplication
class Block(models.Model):
    def calculate_component_mass(self):
        total = 0
        for comp_id, qty in self.components.items():
            component = Component.objects.get(id=comp_id)
            total += component.mass * qty
        return total

class BuildOrder(models.Model):
    def calculate_component_mass(self):
        total = 0
        for block_id, block_qty in self.blocks.items():
            block = Block.objects.get(id=block_id)
            for comp_id, comp_qty in block.components.items():
                component = Component.objects.get(id=comp_id)
                total += component.mass * comp_qty * block_qty
        return total

# AFTER: Extracted utility
def calculate_mass_from_items(items_dict, get_item_func):
    """Generic function to calculate mass from item dictionary"""
    total = 0
    for item_id, quantity in items_dict.items():
        item = get_item_func(item_id)
        total += item.mass * quantity
    return total

class Block(models.Model):
    def calculate_component_mass(self):
        return calculate_mass_from_items(
            self.components,
            lambda id: Component.objects.get(id=id)
        )
```

### Large Class
**Smell**: Class has too many responsibilities
**Fix**: Split into multiple classes

```python
# BEFORE: God class
class BuildOrder(models.Model):
    name = models.CharField(max_length=100)
    blocks = models.JSONField(default=dict)
    
    def calculate_components(self):
        # Complex calculation
        pass
    
    def calculate_ores(self):
        # Complex calculation
        pass
    
    def calculate_mass(self):
        # Complex calculation
        pass
    
    def calculate_cost(self):
        # Complex calculation
        pass
    
    def generate_report(self):
        # Report generation
        pass
    
    def export_to_csv(self):
        # CSV export
        pass
    
    def send_email(self):
        # Email sending
        pass

# AFTER: Separated concerns
class BuildOrder(models.Model):
    """Core model with basic data"""
    name = models.CharField(max_length=100)
    blocks = models.JSONField(default=dict)

class BuildOrderCalculator:
    """Handles all calculations"""
    def __init__(self, build_order):
        self.build_order = build_order
    
    def calculate_components(self):
        pass
    
    def calculate_ores(self):
        pass
    
    def calculate_mass(self):
        pass
    
    def calculate_cost(self):
        pass

class BuildOrderReporter:
    """Handles reporting and export"""
    def __init__(self, build_order):
        self.build_order = build_order
    
    def generate_report(self):
        pass
    
    def export_to_csv(self):
        pass

class BuildOrderNotifier:
    """Handles notifications"""
    def __init__(self, build_order):
        self.build_order = build_order
    
    def send_email(self):
        pass
```

### Long Parameter List
**Smell**: Function has too many parameters (>3-4)
**Fix**: Use parameter object or builder pattern

```python
# BEFORE: Too many parameters
def create_block(name, mass, description, category, tier, 
                 components, pcu_cost, build_time, unlock_level):
    return Block.objects.create(
        name=name,
        mass=mass,
        description=description,
        category=category,
        tier=tier,
        components=components,
        pcu_cost=pcu_cost,
        build_time=build_time,
        unlock_level=unlock_level
    )

# AFTER: Parameter object
from dataclasses import dataclass

@dataclass
class BlockData:
    name: str
    mass: float
    description: str
    category: str
    tier: int
    components: dict
    pcu_cost: int
    build_time: float
    unlock_level: int

def create_block(block_data: BlockData):
    return Block.objects.create(**block_data.__dict__)

# Usage
block_data = BlockData(
    name="Light Armor",
    mass=10.0,
    description="Basic armor",
    category="armor",
    tier=1,
    components={},
    pcu_cost=100,
    build_time=5.0,
    unlock_level=1
)
create_block(block_data)
```

### Magic Numbers
**Smell**: Unexplained numeric literals
**Fix**: Use named constants

```python
# BEFORE: Magic numbers
def calculate_build_time(blocks):
    return len(blocks) * 5.5 + 120

def calculate_cost(components):
    return sum(c.cost * 1.15 for c in components)

# AFTER: Named constants
SECONDS_PER_BLOCK = 5.5
BASE_BUILD_TIME = 120
TAX_RATE = 0.15

def calculate_build_time(blocks):
    return len(blocks) * SECONDS_PER_BLOCK + BASE_BUILD_TIME

def calculate_cost(components):
    return sum(c.cost * (1 + TAX_RATE) for c in components)
```

## Refactoring Patterns

### Extract Method
**When**: Method is too long or does multiple things
**How**: Extract code into new method with descriptive name

```python
# BEFORE
def process_order(order):
    # Validate
    if not order.items:
        raise ValueError("Empty order")
    
    # Calculate
    total = sum(item.price * item.quantity for item in order.items)
    
    # Apply discount
    if total > 100:
        total *= 0.9
    
    return total

# AFTER
def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    total = apply_discount(total)
    return total

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")

def calculate_total(order):
    return sum(item.price * item.quantity for item in order.items)

def apply_discount(total):
    if total > 100:
        return total * 0.9
    return total
```

### Replace Conditional with Polymorphism
**When**: Complex conditionals based on type
**How**: Use inheritance or strategy pattern

```python
# BEFORE: Type checking
def calculate_cost(item):
    if item.type == 'ore':
        return item.mass * 1.0
    elif item.type == 'component':
        return item.mass * 2.5
    elif item.type == 'block':
        return item.mass * 5.0
    else:
        raise ValueError("Unknown type")

# AFTER: Polymorphism
class Ore(models.Model):
    def calculate_cost(self):
        return self.mass * 1.0

class Component(models.Model):
    def calculate_cost(self):
        return self.mass * 2.5

class Block(models.Model):
    def calculate_cost(self):
        return self.mass * 5.0

# Usage
item.calculate_cost()  # Polymorphic call
```

### Introduce Parameter Object
**When**: Functions pass around same group of parameters
**How**: Create class to hold related parameters

```python
# BEFORE: Parameter groups
def create_report(start_date, end_date, user_id, format, include_details):
    pass

def send_report(start_date, end_date, user_id, format, include_details, email):
    pass

def save_report(start_date, end_date, user_id, format, include_details, filename):
    pass

# AFTER: Parameter object
@dataclass
class ReportConfig:
    start_date: date
    end_date: date
    user_id: int
    format: str
    include_details: bool

def create_report(config: ReportConfig):
    pass

def send_report(config: ReportConfig, email: str):
    pass

def save_report(config: ReportConfig, filename: str):
    pass
```

### Replace Magic Number with Constant
**When**: Numeric literals appear in code
**How**: Define named constants

```python
# BEFORE
def calculate_shipping(weight):
    if weight < 5:
        return 10
    elif weight < 20:
        return 25
    else:
        return 50

# AFTER
LIGHT_PACKAGE_WEIGHT = 5
MEDIUM_PACKAGE_WEIGHT = 20
LIGHT_PACKAGE_COST = 10
MEDIUM_PACKAGE_COST = 25
HEAVY_PACKAGE_COST = 50

def calculate_shipping(weight):
    if weight < LIGHT_PACKAGE_WEIGHT:
        return LIGHT_PACKAGE_COST
    elif weight < MEDIUM_PACKAGE_WEIGHT:
        return MEDIUM_PACKAGE_COST
    else:
        return HEAVY_PACKAGE_COST
```

### Decompose Conditional
**When**: Complex conditional logic
**How**: Extract conditions into named functions

```python
# BEFORE: Complex conditional
if (user.is_authenticated and user.has_permission('edit') and 
    not item.is_locked and item.owner == user):
    # Allow edit
    pass

# AFTER: Named conditions
def can_edit_item(user, item):
    return (is_authorized_user(user) and 
            is_editable_item(item) and 
            is_item_owner(user, item))

def is_authorized_user(user):
    return user.is_authenticated and user.has_permission('edit')

def is_editable_item(item):
    return not item.is_locked

def is_item_owner(user, item):
    return item.owner == user

# Usage
if can_edit_item(user, item):
    # Allow edit
    pass
```

## Django-Specific Refactoring

### Fat Models, Thin Views
```python
# BEFORE: Logic in view
def block_detail(request, pk):
    block = Block.objects.get(pk=pk)
    
    # Calculate total mass
    total_mass = block.mass
    for comp_id, qty in block.components.items():
        component = Component.objects.get(id=comp_id)
        total_mass += component.mass * qty
    
    return render(request, 'block_detail.html', {
        'block': block,
        'total_mass': total_mass
    })

# AFTER: Logic in model
class Block(models.Model):
    def calculate_total_mass(self):
        total = self.mass
        for comp_id, qty in self.components.items():
            component = Component.objects.get(id=comp_id)
            total += component.mass * qty
        return total

def block_detail(request, pk):
    block = Block.objects.get(pk=pk)
    return render(request, 'block_detail.html', {
        'block': block,
        'total_mass': block.calculate_total_mass()
    })
```

### Use Manager Methods
```python
# BEFORE: Query logic in view
def active_blocks(request):
    blocks = Block.objects.filter(
        is_active=True,
        tier__lte=request.user.max_tier
    ).select_related('category').order_by('name')
    return render(request, 'blocks.html', {'blocks': blocks})

# AFTER: Custom manager
class BlockManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)
    
    def for_user(self, user):
        return self.filter(tier__lte=user.max_tier)
    
    def with_category(self):
        return self.select_related('category')

class Block(models.Model):
    objects = BlockManager()

def active_blocks(request):
    blocks = Block.objects.active().for_user(request.user).with_category().order_by('name')
    return render(request, 'blocks.html', {'blocks': blocks})
```

## Refactoring Checklist

### Before Refactoring
- [ ] Tests exist and pass
- [ ] Understand the code being refactored
- [ ] Commit current working state
- [ ] Identify specific code smell
- [ ] Plan refactoring approach

### During Refactoring
- [ ] Make one change at a time
- [ ] Run tests after each change
- [ ] Keep changes small and focused
- [ ] Don't add features while refactoring
- [ ] Maintain existing behavior

### After Refactoring
- [ ] All tests still pass
- [ ] Code is more readable
- [ ] Code is more maintainable
- [ ] No new bugs introduced
- [ ] Commit with clear message

## Refactoring Tools

### IDE Refactoring Features
- Rename (F2 in most IDEs)
- Extract method
- Extract variable
- Inline variable/method
- Move class/function

### Automated Refactoring
```bash
# Use rope for Python refactoring
pip install rope

# Use autoflake to remove unused imports
autoflake --remove-all-unused-imports --in-place file.py

# Use isort to organize imports
isort file.py

# Use black for formatting
black file.py
```

## Common Refactoring Mistakes

### Don't Refactor Without Tests
- Always have tests before refactoring
- Tests verify behavior doesn't change
- Without tests, you're rewriting, not refactoring

### Don't Mix Refactoring with Features
- Refactoring changes structure, not behavior
- Adding features changes behavior
- Do them in separate commits

### Don't Refactor Everything at Once
- Small, incremental changes
- Easier to review
- Easier to revert if needed

### Don't Optimize Prematurely
- Refactor for clarity first
- Optimize only when needed
- Profile before optimizing
