import pytest
from cocomo_py.calculator import calculate
from cocomo_py.models import ProjectMode

# Fixture para dados de teste comuns
@pytest.fixture
def sample_drivers():
    """Retorna um dicionário de drivers para o modo intermediário."""
    return {"rely": "high", "cplx": "vhigh"}

def test_calculate_basic_organic():
    """Testa um cálculo simples no modo Orgânico."""
    result = calculate(
        kloc=10,
        mode=ProjectMode.ORGANIC,
        cost_per_month=10000
    )
    assert result.is_intermediate is False
    assert result.mode == ProjectMode.ORGANIC
    assert result.eaf == 1.0
    assert result.effort_person_months == pytest.approx(26.93, rel=1e-2)
    assert result.development_time_months == pytest.approx(8.74, rel=1e-2)
    assert result.people_required == pytest.approx(3.08, rel=1e-2)
    assert result.total_cost == pytest.approx(269315.37, rel=1e-2)

def test_calculate_basic_semi_detached():
    """Testa um cálculo simples no modo Semi-Acoplado."""
    result = calculate(
        kloc=50,
        mode=ProjectMode.SEMI_DETACHED,
        cost_per_month=8000
    )
    assert result.is_intermediate is False
    assert result.effort_person_months == pytest.approx(239.87, rel=1e-2)
    assert result.development_time_months == pytest.approx(17.02, rel=1e-2)
    assert result.total_cost == pytest.approx(1918923.43, rel=1e-2)

def test_calculate_basic_embedded():
    """Testa um cálculo simples no modo Embutido."""
    result = calculate(
        kloc=100,
        mode=ProjectMode.EMBEDDED,
        cost_per_month=12000
    )
    assert result.is_intermediate is False
    assert result.effort_person_months == pytest.approx(904.59, rel=1e-2)
    assert result.development_time_months == pytest.approx(22.08, rel=1e-2)
    assert result.total_cost == pytest.approx(10855110.84, rel=1e-2)

def test_calculate_intermediate_with_drivers(sample_drivers):
    """Testa um cálculo intermediário com drivers de custo."""
    result = calculate(
        kloc=50,
        mode=ProjectMode.SEMI_DETACHED,
        cost_per_month=8000,
        drivers=sample_drivers
    )
    assert result.is_intermediate is True
    assert result.eaf == pytest.approx(1.15 * 1.30, 0.001)  # rely=high * cplx=vhigh
    assert result.effort_person_months == pytest.approx(358.60, rel=1e-2)
    assert result.development_time_months == pytest.approx(19.59, rel=1e-2)
    assert result.total_cost == pytest.approx(2868790.64, rel=1e-2)

def test_invalid_mode():
    """Testa se uma exceção é levantada para um modo inválido."""
    with pytest.raises(ValueError, match="Modo 'invalid-mode' inválido"):
        calculate(
            kloc=10,
            mode="invalid-mode", # type: ignore
            cost_per_month=10000
        )
