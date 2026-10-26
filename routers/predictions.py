
from fastapi import APIRouter, Depends

from schemas import PredictionRequest, PredictionResponse
from ml.predict import predict_failure
from auth_dependencies import require_roles

router = APIRouter(
    prefix="/predictions",
    tags=["Machine Learning Predictions"]
)


@router.post(
    "/failure",
    response_model=PredictionResponse,
    dependencies=[Depends(require_roles("admin","technician", "engineer"))]
)
def predict_equipment_failure(
    request: PredictionRequest
):
    result = predict_failure(
        air_temperature=request.air_temperature,
        process_temperature=request.process_temperature,
        rotational_speed=request.rotational_speed,
        torque=request.torque,
        tool_wear=request.tool_wear
    )

    return result


