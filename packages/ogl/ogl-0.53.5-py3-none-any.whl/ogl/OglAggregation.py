
from logging import Logger
from logging import getLogger

from wx import DC

from miniogl.Shape import Shape
from ogl.OglAssociation import OglAssociation


class OglAggregation(OglAssociation):
    """
    Graphical link representation of aggregation, (empty diamond, arrow).
    To get a new link, you should use the `OglLinkFactory` and specify
    the kind of link you want, OGL_AGGREGATION for an instance of this class.
    """

    def __init__(self, srcShape, pyutLink, dstShape, srcPos=None, dstPos=None):
        """

        Args:
            srcShape:   Source shape
            pyutLink:   Conceptual links associated with the graphical links.
            dstShape:   Destination shape
            srcPos:     Position of source      Override location of input source
            dstPos:     Position of destination Override location of input destination
        """
        super().__init__(srcShape, pyutLink, dstShape, dstPos=dstPos, srcPos=srcPos)

        self.logger: Logger = getLogger(__name__)
        self.SetDrawArrow(True)

    def Draw(self, dc: DC, withChildren: bool = False):
        """
        Called for contents drawing of links.

        @param  dc : Device context
        @param withChildren

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        super().Draw(dc, withChildren)

        # Draw losange
        self.drawLosange(dc, False)

    def __repr__(self):

        srcShape:  Shape = self.getSourceShape()
        destShape: Shape = self.getDestinationShape()
        sourceId:  int   = srcShape.GetID()
        destId:    int   = destShape.GetID()

        return f'OglAggregation - from: id: {sourceId} {self.getSourceShape()} to: id: {destId} {self.getDestinationShape()}'
