from pydantic import BaseModel, PositiveFloat, PositiveInt, computed_field


class TargetConfig(BaseModel):
    name: str
    url: str
    timeout: PositiveFloat
    expected_status: PositiveInt


class CheckResult(BaseModel):
    response_time: PositiveFloat | None
    actual_status_code: PositiveInt | None
    expected_status: PositiveInt | None
    error: str | None

    @computed_field
    def is_healthy(self) -> bool:
        if self.actual_status_code:
            return self.actual_status_code == self.expected_status
        else:
            return False
