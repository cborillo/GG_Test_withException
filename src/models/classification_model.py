from pydantic import BaseModel, Field


class Criterion(BaseModel):
    score: float = Field(
        ...,
        ge=0.1,
        le=1.0,
        description="Clarity score between 0.1 and 1.0",
    )
    explanation: str


class ImageClarityAssessment(BaseModel):
    text_legibility: Criterion
    image_sharpness: Criterion
    contrast: Criterion
    noise_level: Criterion
    text_alignment: Criterion
    overall_clarity_score: float = Field(
        ...,
        ge=0.1,
        le=1.0,
        description="Overall clarity score between 0.1 and 1.0",
    )
    conclusion: str


class Classification(BaseModel):
    type: str = Field(description="the type of the health benefit claim")
    justification: str = Field(description="the justification for the classification")
    # clairity: ImageClarityAssessment

    def should_skip_extraction(self) -> bool:
        return self.type in (
            "Supporting Document",
            "Extended Health Claim Form (Page 2)",
            "Prescription Drug Authorization Form (Other Pages)",
        )

    def get_ocr_model(self) -> str:
        if self.type in (
            "Extended Health Claim Form (Page 1)",
            "Standard Dental Claim Form",
            "Dental Explanation of Benefits",
        ):
            return "prebuilt-layout"
        return "prebuilt-read"
